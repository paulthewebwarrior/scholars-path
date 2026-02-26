from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..career_services import (
    get_career_skill_areas,
    get_subjects_for_skill,
    list_careers,
    resolve_career_by_name,
)
from ..database import get_db
from ..deps import get_current_user
from ..models import CareerSkill, SkillArea, User
from ..schemas import CareerResponse, CareerSkillAreaResponse, CareerSubjectResponse

router = APIRouter(prefix='/api/careers', tags=['careers'])


@router.get('', response_model=list[CareerResponse])
def get_careers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CareerResponse]:
    del current_user
    careers = list_careers(db)
    return [CareerResponse.model_validate(career) for career in careers]


@router.get('/{career_name}', response_model=CareerResponse)
def get_career(
    career_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CareerResponse:
    del current_user
    career = resolve_career_by_name(db, career_name)
    if career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Career not found')
    return CareerResponse.model_validate(career)


@router.get('/{career_name}/skills', response_model=list[CareerSkillAreaResponse])
def get_career_skills(
    career_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CareerSkillAreaResponse]:
    del current_user
    career = resolve_career_by_name(db, career_name)
    if career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Career not found')

    skill_areas = get_career_skill_areas(db, career.id)
    return [
        CareerSkillAreaResponse(
            id=area.id,
            name=area.name,
            description=area.description,
            importance_level=area.importance_level,
        )
        for area in skill_areas
    ]


@router.get('/{career_name}/skills/{skill_id}/subjects', response_model=list[CareerSubjectResponse])
def get_career_skill_subjects(
    career_name: str,
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CareerSubjectResponse]:
    career = resolve_career_by_name(db, career_name)
    if career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Career not found')

    skill_belongs_to_career = db.scalar(
        select(CareerSkill).where(
            CareerSkill.career_id == career.id,
            CareerSkill.skill_area_id == skill_id,
        )
    )
    if skill_belongs_to_career is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found for this career')

    skill = db.scalar(select(SkillArea).where(SkillArea.id == skill_id))
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found')

    subjects = get_subjects_for_skill(db, skill_id, user_course=current_user.course)
    return [
        CareerSubjectResponse(
            id=subject.id,
            name=subject.name,
            field_of_study=subject.field_of_study,
            description=subject.description,
            relevance_indicator=subject.relevance_indicator,
        )
        for subject in subjects
    ]
