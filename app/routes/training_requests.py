from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, RoleChecker
from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.training_request import (
    TrainingRequestCreate,
    TrainingRequestUpdate,
    TrainingRequestResponse,
    TrainingRequestDetailResponse,
)
from app.services import request_service

router = APIRouter()

# Role checkers
allow_trainee = RoleChecker(allowed_roles=[UserRole.TRAINEE.value])
allow_trainer = RoleChecker(allowed_roles=[UserRole.TRAINER.value])


@router.post(
    "/",
    response_model=TrainingRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit training request",
    description="Allows trainees to apply for field experience with a specific trainer.",
)
def create_request(
    request_in: TrainingRequestCreate,
    current_user: User = Depends(allow_trainee),
    db: Session = Depends(get_db),
):
    return request_service.create_training_request(
        db=db, trainee_id=current_user.id, request_in=request_in
    )


@router.get(
    "/",
    response_model=List[TrainingRequestDetailResponse],
    summary="List training requests",
    description="Retrieve all requests relevant to the user. Trainees see their sent applications; Trainers see received offers; Admins see all.",
)
def read_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return request_service.get_requests_by_user(
        db=db, user_id=current_user.id, role=current_user.role
    )


@router.patch(
    "/{request_id}",
    response_model=TrainingRequestResponse,
    summary="Update request status",
    description="Allows a trainer to accept or reject an application. Trainees cannot perform this action.",
)
def update_request(
    request_id: UUID,
    status_in: TrainingRequestUpdate,
    current_user: User = Depends(allow_trainer),
    db: Session = Depends(get_db),
):
    return request_service.update_request_status(
        db=db,
        trainer_id=current_user.id,
        request_id=request_id,
        new_status=status_in.status,
    )
