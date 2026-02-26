from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..career_services import get_user_career_aligned_recommendations, parse_simulation_metrics
from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..schemas import (
    CareerAlignedRecommendationResponse,
    CareerAlignedRecommendationsListResponse,
    CareerResponse,
    SubjectResourceResponse,
)

router = APIRouter(prefix='/api/users', tags=['career-recommendations'])


def _validate_user_access(user_id: int, current_user: User) -> None:
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')


@router.get('/{user_id}/recommendations/career-aligned', response_model=CareerAlignedRecommendationsListResponse)
def get_career_aligned_recommendations(
    user_id: int,
    study_hours: float | None = Query(default=None, ge=0),
    sleep_hours: float | None = Query(default=None, ge=0),
    phone_usage_hours: float | None = Query(default=None, ge=0),
    social_media_hours: float | None = Query(default=None, ge=0),
    gaming_hours: float | None = Query(default=None, ge=0),
    breaks_per_day: float | None = Query(default=None, ge=0),
    coffee_intake: float | None = Query(default=None, ge=0),
    exercise_minutes: float | None = Query(default=None, ge=0),
    stress_level: float | None = Query(default=None, ge=1, le=10),
    focus_score: float | None = Query(default=None, ge=0, le=100),
    attendance_percentage: float | None = Query(default=None, ge=0, le=100),
    assignments_completed_per_week: float | None = Query(default=None, ge=0),
    final_grade: float | None = Query(default=None, ge=0, le=100),
    limit: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CareerAlignedRecommendationsListResponse:
    _validate_user_access(user_id, current_user)

    simulated_metrics = parse_simulation_metrics(
        {
            'study_hours': study_hours,
            'sleep_hours': sleep_hours,
            'phone_usage_hours': phone_usage_hours,
            'social_media_hours': social_media_hours,
            'gaming_hours': gaming_hours,
            'breaks_per_day': breaks_per_day,
            'coffee_intake': coffee_intake,
            'exercise_minutes': exercise_minutes,
            'stress_level': stress_level,
            'focus_score': focus_score,
            'attendance_percentage': attendance_percentage,
            'assignments_completed_per_week': assignments_completed_per_week,
            'final_grade': final_grade,
        }
    )

    career, recommendations = get_user_career_aligned_recommendations(
        db,
        current_user,
        simulated_metrics=simulated_metrics or None,
        limit=limit,
    )

    items = [
        CareerAlignedRecommendationResponse(
            subject_id=item.subject_id,
            subject_name=item.subject_name,
            field_of_study=item.field_of_study,
            description=item.description,
            relevance_indicator=item.relevance_indicator,
            weakness_score=item.weakness_score,
            baseline_weakness_score=item.baseline_weakness_score,
            gap_closure_percent=item.gap_closure_percent,
            career_relevance_context=item.career_relevance_context,
            supporting_skills=item.supporting_skills,
            resources=[
                SubjectResourceResponse(
                    id=resource.id,
                    title=resource.title,
                    url=resource.url,
                    provider=resource.provider,
                )
                for resource in item.resources
            ],
        )
        for item in recommendations
    ]

    return CareerAlignedRecommendationsListResponse(
        career=CareerResponse.model_validate(career) if career is not None else None,
        items=items,
    )
