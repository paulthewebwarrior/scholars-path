from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Career, User
from ..schemas import (
    CareerSelectionRequest,
    CareerSummaryResponse,
    ProfileUpdateRequest,
    UserProfileResponse,
)

router = APIRouter(prefix='/api/profile', tags=['profile'])


def _profile_response_from_user(db: Session, user: User) -> UserProfileResponse:
    career_response: CareerSummaryResponse | None = None
    if user.career_id is not None:
        career = db.scalar(select(Career).where(Career.id == user.career_id))
        if career is not None:
            career_response = CareerSummaryResponse.model_validate(career)

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        course=user.course,
        year_level=user.year_level,
        career_id=user.career_id,
        career_goal=user.career_goal,
        career=career_response,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get('/me', response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    return _profile_response_from_user(db, current_user)


@router.put('/me', response_model=UserProfileResponse)
def update_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    current_user.name = payload.name
    current_user.course = payload.course
    current_user.year_level = payload.year_level
    current_user.career_goal = payload.career_goal

    try:
        db.commit()
        db.refresh(current_user)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to update profile',
        ) from exc

    return _profile_response_from_user(db, current_user)


@router.post('/career', response_model=UserProfileResponse)
def set_career(
    payload: CareerSelectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    career = db.scalar(select(Career).where(Career.id == payload.career_id))
    if career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Career not found')

    current_user.career_id = career.id
    current_user.career_goal = career.name

    try:
        db.commit()
        db.refresh(current_user)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to save selected career',
        ) from exc

    return _profile_response_from_user(db, current_user)


@router.put('/career', response_model=UserProfileResponse)
def update_career(
    payload: CareerSelectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserProfileResponse:
    career = db.scalar(select(Career).where(Career.id == payload.career_id))
    if career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Career not found')

    current_user.career_id = career.id
    current_user.career_goal = career.name

    try:
        db.commit()
        db.refresh(current_user)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Unable to update selected career',
        ) from exc

    return _profile_response_from_user(db, current_user)
