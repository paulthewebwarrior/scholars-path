from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import Subject, SubjectResource, User
from ..schemas import SubjectResourceResponse

router = APIRouter(prefix='/api/resources', tags=['resources'])


@router.get('/subject/{subject_id}', response_model=list[SubjectResourceResponse])
def get_subject_resources(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SubjectResourceResponse]:
    del current_user

    subject = db.scalar(select(Subject).where(Subject.id == subject_id))
    if subject is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Subject not found')

    resources = list(
        db.scalars(
            select(SubjectResource)
            .where(SubjectResource.subject_id == subject_id)
            .order_by(SubjectResource.id.asc())
        ).all()
    )
    return [SubjectResourceResponse.model_validate(resource) for resource in resources]
