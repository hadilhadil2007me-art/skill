from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import RoleChecker
from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewDetailResponse
from app.services import review_service

router = APIRouter()

# Trainee restriction checker
allow_trainee = RoleChecker(allowed_roles=[UserRole.TRAINEE.value])


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a review",
    description="Allows trainees to rate and comment on a trainer's session.",
)
def submit_review(
    review_in: ReviewCreate,
    current_user: User = Depends(allow_trainee),
    db: Session = Depends(get_db),
):
    return review_service.create_review(
        db=db, trainee_id=current_user.id, review_in=review_in
    )


@router.get(
    "/trainer/{trainer_id}",
    response_model=List[ReviewDetailResponse],
    summary="Get trainer reviews",
    description="Retrieve all reviews and comments written about a specific trainer.",
)
def read_trainer_reviews(
    trainer_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return review_service.get_trainer_reviews(
        db=db, trainer_id=trainer_id, skip=skip, limit=limit
    )


@router.get(
    "/trainer/{trainer_id}/rating",
    summary="Get trainer average rating",
    description="Retrieve the average numerical rating (1.0 to 5.0 stars) for a trainer.",
)
def read_trainer_average_rating(trainer_id: UUID, db: Session = Depends(get_db)):
    average = review_service.get_trainer_average_rating(
        db=db, trainer_id=trainer_id
    )
    return {
        "trainer_id": trainer_id,
        "average_rating": average,
    }
