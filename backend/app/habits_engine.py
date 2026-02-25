import logging
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

import joblib
import pandas as pd
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from .models import HabitsAssessment, HabitsCorrelation, HabitsNormalizedExport, HabitsRecommendation

logger = logging.getLogger(__name__)
MODEL_PATH = Path(__file__).resolve().parents[1] / 'artifacts' / 'productivity_detection_model.pkl'

METRIC_NAMES = [
    'study_hours',
    'sleep_hours',
    'phone_usage_hours',
    'social_media_hours',
    'gaming_hours',
    'breaks_per_day',
    'coffee_intake',
    'exercise_minutes',
    'stress_level',
    'focus_score',
    'attendance_percentage',
    'assignments_completed_per_week',
]
NEGATIVE_METRICS = {'phone_usage_hours', 'social_media_hours', 'gaming_hours', 'stress_level'}
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


@dataclass
class CorrelationStat:
    metric_name: str
    performance_metric: str
    correlation_coefficient: float
    sample_size: int
    confidence_interval_low: float
    confidence_interval_high: float
    confidence_level: float
    p_value: float


class PearsonCorrelationCalculator:
    @staticmethod
    def _mean(values: list[float]) -> float:
        return sum(values) / len(values)

    @staticmethod
    def _sample_std(values: list[float], mean: float) -> float:
        if len(values) < 2:
            return 0.0
        variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
        return math.sqrt(variance)

    def calculate(self, x: list[float], y: list[float], confidence_level: float = 95.0) -> CorrelationStat | None:
        if len(x) != len(y) or len(x) < 4:
            return None

        x_mean = self._mean(x)
        y_mean = self._mean(y)
        x_std = self._sample_std(x, x_mean)
        y_std = self._sample_std(y, y_mean)

        if x_std == 0 or y_std == 0:
            return None

        covariance = sum((xv - x_mean) * (yv - y_mean) for xv, yv in zip(x, y, strict=True)) / (len(x) - 1)
        r = max(min(covariance / (x_std * y_std), 1.0), -1.0)
        n = len(x)

        if abs(r) == 1.0:
            p_value = 0.0
            ci_low = r
            ci_high = r
        else:
            t_stat = abs(r) * math.sqrt((n - 2) / (1 - r**2))
            # Normal approximation for p-value; sufficient for this initial implementation.
            p_value = 2 * (1 - 0.5 * (1 + math.erf(t_stat / math.sqrt(2))))

            z = 0.5 * math.log((1 + r) / (1 - r))
            z_delta = 1.96 / math.sqrt(n - 3)
            ci_low = math.tanh(z - z_delta)
            ci_high = math.tanh(z + z_delta)

        return CorrelationStat(
            metric_name='',
            performance_metric='',
            correlation_coefficient=r,
            sample_size=n,
            confidence_interval_low=ci_low,
            confidence_interval_high=ci_high,
            confidence_level=confidence_level,
            p_value=p_value,
        )


class CorrelationCache:
    def __init__(self) -> None:
        self._lock = Lock()
        self._state: tuple[int, int] | None = None

    def should_recompute(self, signature: tuple[int, int]) -> bool:
        with self._lock:
            if self._state == signature:
                return False
            self._state = signature
            return True


correlation_cache = CorrelationCache()
_model_lock = Lock()
_detection_model = None


def _normalize(metric_name: str, value: float | None) -> float:
    min_value, max_value = NORMALIZATION_RANGES[metric_name]
    if value is None:
        return 0.0
    clamped = min(max(value, min_value), max_value)
    if max_value == min_value:
        return 0.0
    return (clamped - min_value) / (max_value - min_value)


def _extract_assessment_metric(assessment: HabitsAssessment, metric_name: str) -> float | None:
    return getattr(assessment, metric_name)


def _load_detection_model():
    global _detection_model
    with _model_lock:
        if _detection_model is not None:
            return _detection_model
        if not MODEL_PATH.exists():
            logger.warning('Productivity detection model not found at %s', MODEL_PATH)
            return None
        try:
            _detection_model = joblib.load(MODEL_PATH)
            return _detection_model
        except Exception:
            logger.exception('Failed to load productivity detection model at %s', MODEL_PATH)
            return None


def _assessment_to_model_features(assessment: HabitsAssessment) -> pd.DataFrame:
    # Fill missing features with neutral defaults so we can score existing assessment records.
    # The training pipeline can handle unknown categories through OneHotEncoder(handle_unknown="ignore").
    features = {
        'age': 20,
        'gender': 'Other',
        'study_hours_per_day': float(assessment.study_hours),
        'sleep_hours': float(assessment.sleep_hours),
        'phone_usage_hours': float(assessment.phone_usage_hours),
        'social_media_hours': float(assessment.social_media_hours),
        'youtube_hours': 0.0,
        'gaming_hours': float(assessment.gaming_hours),
        'breaks_per_day': float(assessment.breaks_per_day),
        'coffee_intake_mg': float(assessment.coffee_intake) * 95.0,
        'exercise_minutes': float(assessment.exercise_minutes),
        'assignments_completed': float(assessment.assignments_completed_per_week),
        'attendance_percentage': float(assessment.attendance_percentage),
        'stress_level': float(assessment.stress_level),
        'focus_score': float(assessment.focus_score),
        'final_grade': float(assessment.final_grade) if assessment.final_grade is not None else math.nan,
    }
    return pd.DataFrame([features])


def predict_productivity_score(assessment: HabitsAssessment) -> float | None:
    model = _load_detection_model()
    if model is None:
        return None
    try:
        features = _assessment_to_model_features(assessment)
        prediction = model.predict(features)[0]
        return float(prediction)
    except Exception:
        logger.exception('Failed to predict productivity score for assessment_id=%s', assessment.assessment_id)
        return None


def update_normalized_exports(db: Session, assessments: list[HabitsAssessment]) -> None:
    for assessment in assessments:
        existing = db.scalar(
            select(HabitsNormalizedExport).where(
                HabitsNormalizedExport.assessment_id == assessment.assessment_id,
            )
        )
        payload = {
            'assessment_id': assessment.assessment_id,
            'user_id': assessment.user_id,
            'study_hours': _normalize('study_hours', assessment.study_hours),
            'sleep_hours': _normalize('sleep_hours', assessment.sleep_hours),
            'phone_usage_hours': _normalize('phone_usage_hours', assessment.phone_usage_hours),
            'social_media_hours': _normalize('social_media_hours', assessment.social_media_hours),
            'gaming_hours': _normalize('gaming_hours', assessment.gaming_hours),
            'breaks_per_day': _normalize('breaks_per_day', assessment.breaks_per_day),
            'coffee_intake': _normalize('coffee_intake', assessment.coffee_intake),
            'exercise_minutes': _normalize('exercise_minutes', assessment.exercise_minutes),
            'stress_level': _normalize('stress_level', assessment.stress_level),
            'focus_score': _normalize('focus_score', assessment.focus_score),
            'attendance_percentage': _normalize('attendance_percentage', assessment.attendance_percentage),
            'assignments_completed_per_week': _normalize(
                'assignments_completed_per_week',
                assessment.assignments_completed_per_week,
            ),
            'final_grade': _normalize('final_grade', assessment.final_grade),
        }
        if existing is None:
            db.add(HabitsNormalizedExport(**payload))
        else:
            for key, value in payload.items():
                setattr(existing, key, value)


def recompute_correlations(db: Session) -> list[HabitsCorrelation]:
    assessments = list(db.scalars(select(HabitsAssessment)).all())
    if len(assessments) < 4:
        return []

    last_created = max(assessment.created_at for assessment in assessments)
    signature = (len(assessments), int(last_created.timestamp()))
    if not correlation_cache.should_recompute(signature):
        return list(db.scalars(select(HabitsCorrelation)).all())

    predicted_productivity: dict[int, float] = {}
    for assessment in assessments:
        score = predict_productivity_score(assessment)
        if score is not None:
            predicted_productivity[assessment.assessment_id] = score

    performance_rows = [
        assessment
        for assessment in assessments
        if (
            assessment.final_grade is not None
            or assessment.assignments_completed_per_week is not None
            or assessment.assessment_id in predicted_productivity
        )
    ]
    if len(performance_rows) < 4:
        return []

    db.execute(delete(HabitsCorrelation))
    calculator = PearsonCorrelationCalculator()
    new_correlations: list[HabitsCorrelation] = []

    for performance_metric in ('predicted_productivity_score', 'final_grade', 'assignments_completed_per_week'):
        for metric_name in METRIC_NAMES:
            x_values: list[float] = []
            y_values: list[float] = []
            for assessment in performance_rows:
                x_val = _extract_assessment_metric(assessment, metric_name)
                if performance_metric == 'predicted_productivity_score':
                    y_val = predicted_productivity.get(assessment.assessment_id)
                else:
                    y_val = _extract_assessment_metric(assessment, performance_metric)
                if x_val is None or y_val is None:
                    continue
                x_values.append(float(x_val))
                y_values.append(float(y_val))

            result = calculator.calculate(x_values, y_values)
            if result is None:
                continue
            correlation = HabitsCorrelation(
                metric_name=metric_name,
                performance_metric=performance_metric,
                correlation_coefficient=result.correlation_coefficient,
                sample_size=result.sample_size,
                confidence_interval_low=result.confidence_interval_low,
                confidence_interval_high=result.confidence_interval_high,
                confidence_level=result.confidence_level,
                p_value=result.p_value,
                calculation_timestamp=datetime.now(timezone.utc),
            )
            db.add(correlation)
            new_correlations.append(correlation)

    update_normalized_exports(db, assessments)
    db.commit()
    logger.info('Recomputed %s correlations from %s assessments', len(new_correlations), len(assessments))
    return new_correlations


def run_correlation_batch(db: Session, cadence: str = 'weekly') -> int:
    correlations = recompute_correlations(db)
    logger.info('Correlation batch run complete cadence=%s rows=%s', cadence, len(correlations))
    return len(correlations)


class RecommendationGenerator:
    def generate(
        self,
        assessment: HabitsAssessment,
        correlations: list[HabitsCorrelation],
    ) -> list[HabitsRecommendation]:
        final_grade_correlation_by_metric = {
            correlation.metric_name: correlation
            for correlation in correlations
            if correlation.performance_metric == 'final_grade'
        }
        productivity_correlation_by_metric = {
            correlation.metric_name: correlation
            for correlation in correlations
            if correlation.performance_metric == 'predicted_productivity_score'
        }
        correlation_by_metric = (
            productivity_correlation_by_metric if productivity_correlation_by_metric else final_grade_correlation_by_metric
        )
        recommendations: list[tuple[str, str, float]] = []

        sleep_corr = correlation_by_metric.get('sleep_hours')
        if (
            sleep_corr is not None
            and assessment.sleep_hours < 7
            and sleep_corr.correlation_coefficient > 0.4
        ):
            recommendations.append(
                (
                    'Increase sleep to 7-8 hours per night for better focus and grades',
                    'sleep_hours',
                    abs(sleep_corr.correlation_coefficient),
                )
            )

        phone_corr = correlation_by_metric.get('phone_usage_hours')
        if (
            phone_corr is not None
            and assessment.phone_usage_hours > 4
            and phone_corr.correlation_coefficient < -0.3
        ):
            recommendations.append(
                (
                    'Reduce phone usage during study sessions - consider using app blockers',
                    'phone_usage_hours',
                    abs(phone_corr.correlation_coefficient),
                )
            )

        exercise_corr = correlation_by_metric.get('exercise_minutes')
        if (
            exercise_corr is not None
            and assessment.exercise_minutes < 30
            and exercise_corr.correlation_coefficient > 0.3
        ):
            recommendations.append(
                (
                    'Add 30+ minutes of daily exercise to improve focus and energy levels',
                    'exercise_minutes',
                    abs(exercise_corr.correlation_coefficient),
                )
            )

        social_corr = correlation_by_metric.get('social_media_hours')
        if (
            social_corr is not None
            and assessment.social_media_hours > 2
            and social_corr.correlation_coefficient < -0.3
        ):
            recommendations.append(
                (
                    'Limit social media to 30-60 minutes daily during study breaks only',
                    'social_media_hours',
                    abs(social_corr.correlation_coefficient),
                )
            )

        study_corr = correlation_by_metric.get('study_hours')
        if (
            study_corr is not None
            and assessment.study_hours < 2
            and study_corr.correlation_coefficient > 0.3
        ):
            recommendations.append(
                (
                    'Increase focused study time to 2-3 hours daily in consistent blocks',
                    'study_hours',
                    abs(study_corr.correlation_coefficient),
                )
            )

        if len(recommendations) < 3:
            ranked = sorted(
                (
                    correlation
                    for correlation in correlation_by_metric.values()
                    if abs(correlation.correlation_coefficient) >= 0.3
                ),
                key=lambda item: abs(item.correlation_coefficient),
                reverse=True,
            )
            for correlation in ranked:
                direction = 'increase' if correlation.metric_name not in NEGATIVE_METRICS else 'reduce'
                recommendations.append(
                    (
                        f'Consider adjusting {correlation.metric_name.replace("_", " ")} to {direction} for better outcomes',
                        correlation.metric_name,
                        abs(correlation.correlation_coefficient),
                    )
                )
                if len(recommendations) >= 5:
                    break

        deduped: list[tuple[str, str, float]] = []
        seen_text: set[str] = set()
        for recommendation in sorted(recommendations, key=lambda item: item[2], reverse=True):
            if recommendation[0] in seen_text:
                continue
            deduped.append(recommendation)
            seen_text.add(recommendation[0])
            if len(deduped) >= 5:
                break
        return [
            HabitsRecommendation(
                assessment_id=assessment.assessment_id,
                user_id=assessment.user_id,
                recommendation_text=text,
                supporting_metric=metric,
                correlation_strength=strength,
                priority_rank=index + 1,
            )
            for index, (text, metric, strength) in enumerate(deduped[:5])
        ]
