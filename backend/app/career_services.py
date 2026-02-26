from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from .career_catalog import (
    CAREER_DEFINITIONS,
    CAREER_TO_SKILLS,
    SKILL_AREA_DEFINITIONS,
    SKILL_METRIC_RULES,
    SKILL_TO_SUBJECTS,
    SUBJECT_DEFINITIONS,
    SUBJECT_RESOURCES,
    slugify_name,
)
from .models import (
    Career,
    CareerSkill,
    HabitsAssessment,
    SkillArea,
    SkillSubject,
    Subject,
    SubjectResource,
    User,
)

HIGHER_IS_BETTER_DEFAULTS = {
    'study_hours': True,
    'sleep_hours': True,
    'phone_usage_hours': False,
    'social_media_hours': False,
    'gaming_hours': False,
    'breaks_per_day': True,
    'coffee_intake': False,
    'exercise_minutes': True,
    'stress_level': False,
    'focus_score': True,
    'attendance_percentage': True,
    'assignments_completed_per_week': True,
    'final_grade': True,
}

NORMALIZATION_RANGES = {
    'study_hours': (0.0, 12.0),
    'sleep_hours': (0.0, 12.0),
    'phone_usage_hours': (0.0, 12.0),
    'social_media_hours': (0.0, 10.0),
    'gaming_hours': (0.0, 10.0),
    'breaks_per_day': (0.0, 20.0),
    'coffee_intake': (0.0, 10.0),
    'exercise_minutes': (0.0, 180.0),
    'stress_level': (1.0, 10.0),
    'focus_score': (0.0, 100.0),
    'attendance_percentage': (0.0, 100.0),
    'assignments_completed_per_week': (0.0, 20.0),
    'final_grade': (0.0, 100.0),
}

IMPORTANCE_WEIGHTS = {
    'critical': 1.0,
    'high': 0.8,
    'moderate': 0.6,
}

FIELD_ALIASES = {
    'computer science': {
        'computer science',
        'information technology',
        'software engineering',
        'data science',
        'cybersecurity',
    },
    'data science': {
        'data science',
        'computer science',
        'statistics',
        'business analytics',
        'information technology',
    },
    'business': {
        'business',
        'management',
        'economics',
        'marketing',
        'accounting',
    },
    'medicine': {
        'medicine',
        'medical technology',
        'biology',
        'nursing',
        'health sciences',
    },
    'engineering': {
        'engineering',
        'mechanical',
        'civil',
        'electrical',
        'chemical',
        'industrial',
    },
}


@dataclass(frozen=True)
class SubjectResourceDTO:
    id: int
    title: str
    url: str
    provider: str


@dataclass(frozen=True)
class CareerSkillAreaDTO:
    id: int
    name: str
    description: str
    importance_level: str


@dataclass(frozen=True)
class CareerSubjectDTO:
    id: int
    name: str
    field_of_study: str
    description: str
    relevance_indicator: str


@dataclass(frozen=True)
class CareerAlignedRecommendationDTO:
    subject_id: int
    subject_name: str
    field_of_study: str
    description: str
    relevance_indicator: str
    weakness_score: float
    baseline_weakness_score: float
    gap_closure_percent: float
    career_relevance_context: str
    supporting_skills: list[str]
    resources: list[SubjectResourceDTO]


@dataclass
class _SubjectAccumulator:
    subject: Subject
    relevance_indicator: str
    current_score: float
    baseline_score: float
    importance_level: str
    supporting_skills: set[str]


def _normalize(metric_name: str, value: float | None) -> float:
    if value is None:
        return 0.5
    min_value, max_value = NORMALIZATION_RANGES.get(metric_name, (0.0, 1.0))
    if max_value == min_value:
        return 0.5
    clamped = max(min(value, max_value), min_value)
    return (clamped - min_value) / (max_value - min_value)


def _is_higher_better(metric_name: str) -> bool:
    return HIGHER_IS_BETTER_DEFAULTS.get(metric_name, True)


def _get_metric_value(
    assessment: HabitsAssessment,
    metric_name: str,
    simulated_metrics: dict[str, float] | None,
) -> float | None:
    if simulated_metrics and metric_name in simulated_metrics:
        return simulated_metrics[metric_name]
    value = getattr(assessment, metric_name, None)
    if value is None:
        return None
    return float(value)


def _skill_weakness_score(
    assessment: HabitsAssessment,
    skill_name: str,
    simulated_metrics: dict[str, float] | None = None,
) -> float:
    rules = SKILL_METRIC_RULES.get(skill_name)
    if not rules:
        return 0.5

    weighted_total = 0.0
    weight_sum = 0.0
    for rule in rules:
        raw_value = _get_metric_value(assessment, rule.metric_name, simulated_metrics)
        normalized = _normalize(rule.metric_name, raw_value)
        weakness = (1 - normalized) if rule.higher_is_better else normalized
        weighted_total += weakness * rule.weight
        weight_sum += rule.weight

    if weight_sum == 0:
        return 0.5
    return max(0.0, min(1.0, weighted_total / weight_sum))


def _is_cross_disciplinary(field: str) -> bool:
    normalized = field.strip().lower()
    return normalized in {'general', 'cross-disciplinary', 'cross disciplinary'}


def course_matches_field(course: str, field: str) -> bool:
    if _is_cross_disciplinary(field):
        return True

    normalized_course = course.strip().lower()
    normalized_field = field.strip().lower()
    if not normalized_course:
        return True

    if normalized_field in normalized_course or normalized_course in normalized_field:
        return True

    field_aliases = FIELD_ALIASES.get(normalized_field, {normalized_field})
    for alias in field_aliases:
        if alias in normalized_course:
            return True

    course_tokens = set(normalized_course.replace('-', ' ').split())
    for alias in field_aliases:
        if course_tokens.intersection(alias.split()):
            return True

    return False


def _find_by_name_ci(items: list[dict[str, str]], name: str) -> dict[str, str] | None:
    target = name.strip().lower()
    for item in items:
        if item['name'].lower() == target:
            return item
    return None


def seed_career_metadata(db: Session) -> None:
    existing_careers = {career.name: career for career in db.scalars(select(Career)).all()}
    existing_skills = {skill.name: skill for skill in db.scalars(select(SkillArea)).all()}
    existing_subjects = {
        (subject.name, subject.field_of_study): subject for subject in db.scalars(select(Subject)).all()
    }

    for career_data in CAREER_DEFINITIONS:
        career = existing_careers.get(career_data['name'])
        if career is None:
            career = Career(
                name=career_data['name'],
                description=career_data['description'],
            )
            db.add(career)
            db.flush()
            existing_careers[career.name] = career

    for skill_data in SKILL_AREA_DEFINITIONS:
        skill = existing_skills.get(skill_data['name'])
        if skill is None:
            skill = SkillArea(
                name=skill_data['name'],
                description=skill_data['description'],
                importance_level=skill_data['importance_level'],
            )
            db.add(skill)
            db.flush()
            existing_skills[skill.name] = skill

    for subject_data in SUBJECT_DEFINITIONS:
        key = (subject_data['name'], subject_data['field_of_study'])
        subject = existing_subjects.get(key)
        if subject is None:
            subject = Subject(
                name=subject_data['name'],
                field_of_study=subject_data['field_of_study'],
                description=subject_data['description'],
            )
            db.add(subject)
            db.flush()
            existing_subjects[key] = subject

    existing_career_skill_pairs = {
        (pair.career_id, pair.skill_area_id)
        for pair in db.scalars(select(CareerSkill)).all()
    }
    for career_name, skill_names in CAREER_TO_SKILLS.items():
        career = existing_careers.get(career_name)
        if career is None:
            continue
        for skill_name in skill_names:
            skill = existing_skills.get(skill_name)
            if skill is None:
                continue
            pair_key = (career.id, skill.id)
            if pair_key in existing_career_skill_pairs:
                continue
            db.add(CareerSkill(career_id=career.id, skill_area_id=skill.id))
            existing_career_skill_pairs.add(pair_key)

    existing_skill_subject_pairs = {
        (pair.skill_area_id, pair.subject_id): pair
        for pair in db.scalars(select(SkillSubject)).all()
    }
    for skill_name, subject_pairs in SKILL_TO_SUBJECTS.items():
        skill = existing_skills.get(skill_name)
        if skill is None:
            continue
        for subject_name, relevance_indicator in subject_pairs:
            subject_data = _find_by_name_ci(SUBJECT_DEFINITIONS, subject_name)
            if subject_data is None:
                continue
            subject = existing_subjects.get((subject_data['name'], subject_data['field_of_study']))
            if subject is None:
                continue
            key = (skill.id, subject.id)
            existing = existing_skill_subject_pairs.get(key)
            if existing is None:
                db.add(
                    SkillSubject(
                        skill_area_id=skill.id,
                        subject_id=subject.id,
                        relevance_indicator=relevance_indicator,
                    )
                )
                continue
            if existing.relevance_indicator != relevance_indicator:
                existing.relevance_indicator = relevance_indicator

    existing_resources_by_subject: dict[int, dict[str, SubjectResource]] = {}
    for resource in db.scalars(select(SubjectResource)).all():
        existing_resources_by_subject.setdefault(resource.subject_id, {})[resource.url] = resource

    for subject_data in SUBJECT_DEFINITIONS:
        subject = existing_subjects.get((subject_data['name'], subject_data['field_of_study']))
        if subject is None:
            continue
        subject_resources = SUBJECT_RESOURCES.get(subject_data['name'], [])
        existing_urls = existing_resources_by_subject.setdefault(subject.id, {})
        for resource_data in subject_resources:
            if resource_data['url'] in existing_urls:
                continue
            resource = SubjectResource(
                subject_id=subject.id,
                title=resource_data['title'],
                url=resource_data['url'],
                provider=resource_data['provider'],
            )
            db.add(resource)
            existing_urls[resource.url] = resource

    db.commit()


def resolve_career_by_name(db: Session, career_name: str) -> Career | None:
    normalized = career_name.strip().lower()
    careers = list(db.scalars(select(Career)).all())
    for career in careers:
        if career.name.lower() == normalized:
            return career
        if slugify_name(career.name) == normalized:
            return career
    return None


def list_careers(db: Session) -> list[Career]:
    return list(db.scalars(select(Career).order_by(Career.name.asc())).all())


def get_career_skill_areas(db: Session, career_id: int) -> list[CareerSkillAreaDTO]:
    rows = db.execute(
        select(SkillArea)
        .join(CareerSkill, CareerSkill.skill_area_id == SkillArea.id)
        .where(CareerSkill.career_id == career_id)
        .order_by(SkillArea.name.asc())
    ).scalars().all()
    return [
        CareerSkillAreaDTO(
            id=row.id,
            name=row.name,
            description=row.description,
            importance_level=row.importance_level,
        )
        for row in rows
    ]


def get_subjects_for_skill(
    db: Session,
    skill_id: int,
    *,
    user_course: str | None = None,
) -> list[CareerSubjectDTO]:
    rows = db.execute(
        select(SkillSubject, Subject)
        .join(Subject, Subject.id == SkillSubject.subject_id)
        .where(SkillSubject.skill_area_id == skill_id)
        .order_by(Subject.name.asc())
    ).all()

    filtered: list[CareerSubjectDTO] = []
    for link, subject in rows:
        if user_course and not course_matches_field(user_course, subject.field_of_study):
            continue
        filtered.append(
            CareerSubjectDTO(
                id=subject.id,
                name=subject.name,
                field_of_study=subject.field_of_study,
                description=subject.description,
                relevance_indicator=link.relevance_indicator,
            )
        )
    return filtered


def _score_subjects_for_skills(
    db: Session,
    assessment: HabitsAssessment,
    skills: list[CareerSkillAreaDTO],
    *,
    user_course: str,
    simulated_metrics: dict[str, float] | None,
) -> dict[int, _SubjectAccumulator]:
    skill_ids = [skill.id for skill in skills]
    if not skill_ids:
        return {}

    rows = db.execute(
        select(SkillSubject, Subject)
        .join(Subject, Subject.id == SkillSubject.subject_id)
        .where(SkillSubject.skill_area_id.in_(skill_ids))
    ).all()

    skill_by_id = {skill.id: skill for skill in skills}
    accumulators: dict[int, _SubjectAccumulator] = {}

    for link, subject in rows:
        skill = skill_by_id.get(link.skill_area_id)
        if skill is None:
            continue
        if user_course and not course_matches_field(user_course, subject.field_of_study):
            continue

        skill_weakness = _skill_weakness_score(
            assessment,
            skill.name,
            simulated_metrics=simulated_metrics,
        )
        baseline_weakness = _skill_weakness_score(assessment, skill.name, simulated_metrics=None)
        importance_weight = IMPORTANCE_WEIGHTS.get(skill.importance_level, 0.6)
        relevance_weight = IMPORTANCE_WEIGHTS.get(link.relevance_indicator, 0.6)

        current_score = skill_weakness * importance_weight * relevance_weight
        baseline_score = baseline_weakness * importance_weight * relevance_weight

        existing = accumulators.get(subject.id)
        if existing is None:
            accumulators[subject.id] = _SubjectAccumulator(
                subject=subject,
                relevance_indicator=link.relevance_indicator,
                current_score=current_score,
                baseline_score=baseline_score,
                importance_level=skill.importance_level,
                supporting_skills={skill.name},
            )
            continue

        existing.supporting_skills.add(skill.name)
        if current_score > existing.current_score:
            existing.current_score = current_score
            existing.relevance_indicator = link.relevance_indicator
            existing.importance_level = skill.importance_level
        if baseline_score > existing.baseline_score:
            existing.baseline_score = baseline_score

    return accumulators


def _load_resources(db: Session, subject_ids: list[int]) -> dict[int, list[SubjectResourceDTO]]:
    if not subject_ids:
        return {}
    rows = db.scalars(
        select(SubjectResource)
        .where(SubjectResource.subject_id.in_(subject_ids))
        .order_by(SubjectResource.subject_id.asc(), SubjectResource.id.asc())
    ).all()

    grouped: dict[int, list[SubjectResourceDTO]] = {}
    for row in rows:
        grouped.setdefault(row.subject_id, []).append(
            SubjectResourceDTO(
                id=row.id,
                title=row.title,
                url=row.url,
                provider=row.provider,
            )
        )
    return grouped


def get_weak_subjects_for_skills(
    db: Session,
    user_id: int,
    skill_areas: list[CareerSkillAreaDTO],
    *,
    user_course: str,
    simulated_metrics: dict[str, float] | None = None,
    limit: int = 10,
) -> list[CareerAlignedRecommendationDTO]:
    latest_assessment = db.scalar(
        select(HabitsAssessment)
        .where(HabitsAssessment.user_id == user_id)
        .order_by(HabitsAssessment.created_at.desc())
    )
    if latest_assessment is None:
        return []

    scored = _score_subjects_for_skills(
        db,
        latest_assessment,
        skill_areas,
        user_course=user_course,
        simulated_metrics=simulated_metrics,
    )
    if not scored:
        return []

    ranked = sorted(scored.values(), key=lambda item: item.current_score, reverse=True)[:limit]
    resources_by_subject = _load_resources(db, [entry.subject.id for entry in ranked])

    recommendations: list[CareerAlignedRecommendationDTO] = []
    for entry in ranked:
        gap_closure = max(0.0, min(100.0, (entry.baseline_score - entry.current_score) * 100))
        relevance_label = entry.importance_level.capitalize()
        recommendations.append(
            CareerAlignedRecommendationDTO(
                subject_id=entry.subject.id,
                subject_name=entry.subject.name,
                field_of_study=entry.subject.field_of_study,
                description=entry.subject.description,
                relevance_indicator=entry.relevance_indicator,
                weakness_score=round(entry.current_score, 4),
                baseline_weakness_score=round(entry.baseline_score, 4),
                gap_closure_percent=round(gap_closure, 2),
                career_relevance_context=f'{relevance_label} for career readiness',
                supporting_skills=sorted(entry.supporting_skills),
                resources=resources_by_subject.get(entry.subject.id, []),
            )
        )
    return recommendations


def get_user_career_aligned_recommendations(
    db: Session,
    user: User,
    *,
    simulated_metrics: dict[str, float] | None = None,
    limit: int = 3,
) -> tuple[Career | None, list[CareerAlignedRecommendationDTO]]:
    if user.career_id is None:
        return None, []

    career = db.scalar(select(Career).where(Career.id == user.career_id))
    if career is None:
        return None, []

    skill_areas = get_career_skill_areas(db, career.id)
    recommendations = get_weak_subjects_for_skills(
        db,
        user.id,
        skill_areas,
        user_course=user.course,
        simulated_metrics=simulated_metrics,
        limit=limit,
    )

    with_career_context: list[CareerAlignedRecommendationDTO] = []
    for recommendation in recommendations:
        with_career_context.append(
            CareerAlignedRecommendationDTO(
                subject_id=recommendation.subject_id,
                subject_name=recommendation.subject_name,
                field_of_study=recommendation.field_of_study,
                description=recommendation.description,
                relevance_indicator=recommendation.relevance_indicator,
                weakness_score=recommendation.weakness_score,
                baseline_weakness_score=recommendation.baseline_weakness_score,
                gap_closure_percent=recommendation.gap_closure_percent,
                career_relevance_context=f'{recommendation.relevance_indicator.capitalize()} for {career.name}',
                supporting_skills=recommendation.supporting_skills,
                resources=recommendation.resources,
            )
        )

    return career, with_career_context


def parse_simulation_metrics(params: dict[str, str | float | int | None]) -> dict[str, float]:
    parsed: dict[str, float] = {}
    for key, value in params.items():
        if value is None:
            continue
        if key not in NORMALIZATION_RANGES:
            continue
        try:
            parsed[key] = float(value)
        except (TypeError, ValueError):
            continue
    return parsed
