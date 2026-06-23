from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate


def get_review_by_id(db: Session, review_id: UUID) -> Optional[Review]:
    """
    Retrieve a review by its ID.
    """
    return db.query(Review).filter(Review.id == review_id).first()


def get_trainer_reviews(
    db: Session, trainer_id: UUID, skip: int = 0, limit: int = 100
) -> List[Review]:
    """
    Retrieve reviews received by a trainer.
    """
    return (
        db.query(Review)
        .filter(Review.trainer_id == trainer_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_trainer_average_rating(db: Session, trainer_id: UUID) -> float:
    """
    Calculate the average star rating of a trainer.
    Returns 0.0 if there are no reviews.
    """
    result = (
        db.query(func.avg(Review.rating))
        .filter(Review.trainer_id == trainer_id)
        .scalar()
    )
    return round(float(result), 2) if result is not None else 0.0


def create_review(
    db: Session, trainee_id: UUID, review_in: ReviewCreate
) -> Review:
    """
    Submit a rating and comment for a trainer.
    """
    # 1. Trainee role check
    trainee = db.query(User).filter(User.id == trainee_id).first()
    if not trainee or trainee.role != UserRole.TRAINEE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only trainees can submit reviews.",
        )

    # 2. Prevent self-review (in case of system inconsistencies)
    if trainee_id == review_in.trainer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot review yourself.",
        )

    # 3. Trainer role check
    trainer = db.query(User).filter(User.id == review_in.trainer_id).first()
    if not trainer or trainer.role != UserRole.TRAINER.value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer not found or user is not a trainer.",
        )

    # 4. Check for duplicate review from this trainee
    existing_review = (
        db.query(Review)
        .filter(
            Review.trainee_id == trainee_id,
            Review.trainer_id == review_in.trainer_id,
        )
        .first()
    )
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this trainer. Multiple reviews are not allowed.",
        )

    db_obj = Review(
        trainee_id=trainee_id,
        trainer_id=review_in.trainer_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
