from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.training_request import TrainingRequest, RequestStatus
from app.models.user import User, UserRole
from app.schemas.training_request import TrainingRequestCreate


def get_request_by_id(db: Session, request_id: UUID) -> Optional[TrainingRequest]:
    """
    Retrieve a training request by its ID.
    """
    return db.query(TrainingRequest).filter(TrainingRequest.id == request_id).first()


def get_requests_by_user(
    db: Session, user_id: UUID, role: str
) -> List[TrainingRequest]:
    """
    Retrieve training requests for a user based on their role (trainee or trainer).
    """
    if role == UserRole.TRAINEE.value:
        return (
            db.query(TrainingRequest)
            .filter(TrainingRequest.trainee_id == user_id)
            .order_by(TrainingRequest.created_at.desc())
            .all()
        )
    elif role == UserRole.TRAINER.value:
        return (
            db.query(TrainingRequest)
            .filter(TrainingRequest.trainer_id == user_id)
            .order_by(TrainingRequest.created_at.desc())
            .all()
        )
    else:
        # Admins see all requests
        return (
            db.query(TrainingRequest)
            .order_by(TrainingRequest.created_at.desc())
            .all()
        )


def create_training_request(
    db: Session, trainee_id: UUID, request_in: TrainingRequestCreate
) -> TrainingRequest:
    """
    Create a new training request from a trainee to a trainer.
    """
    # 1. Trainee role check
    trainee = db.query(User).filter(User.id == trainee_id).first()
    if not trainee or trainee.role != UserRole.TRAINEE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only trainees can send training requests.",
        )

    # 2. Trainer role check
    trainer = db.query(User).filter(User.id == request_in.trainer_id).first()
    if not trainer or trainer.role != UserRole.TRAINER.value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found or user is not a trainer.",
        )

    # 3. Check for existing pending request to avoid duplicates
    existing_request = (
        db.query(TrainingRequest)
        .filter(
            TrainingRequest.trainee_id == trainee_id,
            TrainingRequest.trainer_id == request_in.trainer_id,
            TrainingRequest.status == RequestStatus.PENDING.value,
        )
        .first()
    )
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending training request with this trainer.",
        )

    db_obj = TrainingRequest(
        trainee_id=trainee_id,
        trainer_id=request_in.trainer_id,
        message=request_in.message,
        status=RequestStatus.PENDING.value,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_request_status(
    db: Session, trainer_id: UUID, request_id: UUID, new_status: RequestStatus
) -> TrainingRequest:
    """
    Accept or reject a training request (only accessible by the requested trainer).
    """
    request = get_request_by_id(db, request_id=request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training request not found.",
        )

    # Verify that the user attempting to update the status is indeed the trainer
    if request.trainer_id != trainer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this request.",
        )

    if request.status != RequestStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change status of a request that is already {request.status}.",
        )

    request.status = new_status.value
    db.commit()
    db.refresh(request)
    return request
