from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import User
from ..schemas import ProfileUpdateRequest, UserProfileResponse

router = APIRouter(prefix='/api/profile', tags=['profile'])


@router.get('/me', response_model=UserProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)) -> UserProfileResponse:
    return UserProfileResponse.model_validate(current_user)


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

    return UserProfileResponse.model_validate(current_user)
