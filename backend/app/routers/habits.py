import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..habits_engine import RecommendationGenerator, recompute_correlations
from ..models import HabitsAssessment, HabitsCorrelation, HabitsRecommendation, User
from ..schemas import (
    HabitsAssessmentCreate,
    HabitsAssessmentHistoryResponse,
    HabitsAssessmentResponse,
    HabitsCorrelationResponse,
    HabitsRecommendationResponse,
    HabitsRecommendationsListResponse,
)

router = APIRouter(prefix='/api/habits', tags=['habits'])
logger = logging.getLogger(__name__)


def _validate_user_access(user_id: int, current_user: User) -> None:
    if user_id != current_user.id:
        logger.warning(
            'habits.access_denied requested_user_id=%s authenticated_user_id=%s',
            user_id,
            current_user.id,
        )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden')


@router.post('/{user_id}/assessment', response_model=HabitsAssessmentResponse, status_code=status.HTTP_201_CREATED)
def submit_assessment(
    user_id: int,
    payload: HabitsAssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitsAssessmentResponse:
    _validate_user_access(user_id, current_user)
    logger.info('habits.assessment.submit.start user_id=%s', user_id)

    assessment = HabitsAssessment(user_id=user_id, **payload.model_dump())
    db.add(assessment)
    try:
        db.commit()
        db.refresh(assessment)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to store habits assessment',
        ) from exc
    logger.info(
        'habits.assessment.submit.saved user_id=%s assessment_id=%s',
        user_id,
        assessment.assessment_id,
    )

    correlations = recompute_correlations(db)
    if not correlations:
        correlations = list(db.scalars(select(HabitsCorrelation)).all())
    logger.info('habits.assessment.submit.correlations user_id=%s count=%s', user_id, len(correlations))

    generator = RecommendationGenerator()
    recommendations = generator.generate(assessment, correlations)
    for recommendation in recommendations:
        db.add(recommendation)
    db.commit()
    logger.info(
        'habits.assessment.submit.recommendations user_id=%s assessment_id=%s count=%s',
        user_id,
        assessment.assessment_id,
        len(recommendations),
    )

    return HabitsAssessmentResponse.model_validate(assessment)


@router.get('/{user_id}/latest', response_model=HabitsAssessmentResponse)
def get_latest_assessment(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitsAssessmentResponse:
    _validate_user_access(user_id, current_user)
    logger.info('habits.assessment.latest.start user_id=%s', user_id)

    assessment = db.scalar(
        select(HabitsAssessment)
        .where(HabitsAssessment.user_id == user_id)
        .order_by(HabitsAssessment.created_at.desc())
    )
    if assessment is None:
        logger.info('habits.assessment.latest.empty user_id=%s', user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No assessments found')
    logger.info('habits.assessment.latest.success user_id=%s assessment_id=%s', user_id, assessment.assessment_id)
    return HabitsAssessmentResponse.model_validate(assessment)


@router.get('/{user_id}/history', response_model=HabitsAssessmentHistoryResponse)
def get_assessment_history(
    user_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitsAssessmentHistoryResponse:
    _validate_user_access(user_id, current_user)
    logger.info(
        'habits.assessment.history.start user_id=%s page=%s page_size=%s',
        user_id,
        page,
        page_size,
    )

    total = db.scalar(
        select(func.count())
        .select_from(HabitsAssessment)
        .where(HabitsAssessment.user_id == user_id)
    ) or 0

    offset = (page - 1) * page_size
    items = list(
        db.scalars(
            select(HabitsAssessment)
            .where(HabitsAssessment.user_id == user_id)
            .order_by(HabitsAssessment.created_at.desc())
            .offset(offset)
            .limit(page_size)
        ).all()
    )
    return HabitsAssessmentHistoryResponse(
        items=[HabitsAssessmentResponse.model_validate(item) for item in items],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get('/{user_id}/correlations', response_model=list[HabitsCorrelationResponse])
def get_correlations(
    user_id: int,
    min_abs_r: float = Query(default=0.3, ge=0, le=1),
    min_confidence: float = Query(default=95, ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[HabitsCorrelationResponse]:
    _validate_user_access(user_id, current_user)
    logger.info(
        'audit habits-correlations user_id=%s min_abs_r=%s min_confidence=%s',
        user_id,
        min_abs_r,
        min_confidence,
    )

    rows = list(
        db.scalars(
            select(HabitsCorrelation).where(
                func.abs(HabitsCorrelation.correlation_coefficient) >= min_abs_r,
                HabitsCorrelation.confidence_level >= min_confidence,
            )
        ).all()
    )
    logger.info('habits.correlations.success user_id=%s count=%s', user_id, len(rows))
    return [HabitsCorrelationResponse.model_validate(item) for item in rows]


@router.get('/{user_id}/recommendations', response_model=HabitsRecommendationsListResponse)
def get_recommendations(
    user_id: int,
    assessment_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitsRecommendationsListResponse:
    _validate_user_access(user_id, current_user)
    logger.info('audit habits-recommendations user_id=%s assessment_id=%s', user_id, assessment_id)

    query = select(HabitsRecommendation).where(HabitsRecommendation.user_id == user_id)
    if assessment_id is not None:
        query = query.where(HabitsRecommendation.assessment_id == assessment_id)
    else:
        latest_assessment_id = db.scalar(
            select(HabitsAssessment.assessment_id)
            .where(HabitsAssessment.user_id == user_id)
            .order_by(HabitsAssessment.created_at.desc())
            .limit(1)
        )
        if latest_assessment_id is None:
            return HabitsRecommendationsListResponse(items=[])
        query = query.where(HabitsRecommendation.assessment_id == latest_assessment_id)

    items = list(
        db.scalars(
            query.order_by(
                HabitsRecommendation.priority_rank.asc(),
                HabitsRecommendation.created_at.desc(),
            )
        ).all()
    )
    logger.info('habits.recommendations.success user_id=%s count=%s', user_id, len(items))
    return HabitsRecommendationsListResponse(
        items=[HabitsRecommendationResponse.model_validate(item) for item in items]
    )


@router.post('/{user_id}/recommendations/{recommendation_id}/feedback', response_model=HabitsRecommendationResponse)
def update_recommendation_feedback(
    user_id: int,
    recommendation_id: int,
    status_value: str = Query(pattern='^(attempted|completed|not_applicable)$'),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HabitsRecommendationResponse:
    _validate_user_access(user_id, current_user)
    logger.info(
        'habits.recommendation.feedback.start user_id=%s recommendation_id=%s status=%s',
        user_id,
        recommendation_id,
        status_value,
    )

    recommendation = db.scalar(
        select(HabitsRecommendation).where(
            HabitsRecommendation.id == recommendation_id,
            HabitsRecommendation.user_id == user_id,
        )
    )
    if recommendation is None:
        logger.info(
            'habits.recommendation.feedback.not_found user_id=%s recommendation_id=%s',
            user_id,
            recommendation_id,
        )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Recommendation not found')
    recommendation.status = status_value
    recommendation.status_updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(recommendation)
    logger.info(
        'habits.recommendation.feedback.success user_id=%s recommendation_id=%s',
        user_id,
        recommendation_id,
    )
    return HabitsRecommendationResponse.model_validate(recommendation)
