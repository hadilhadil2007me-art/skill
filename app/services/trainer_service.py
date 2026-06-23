from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.trainer_profile import TrainerProfile
from app.models.user import AccountStatus, User, UserRole
from app.models.skill import Skill
from app.schemas.trainer_profile import TrainerProfileCreate, TrainerProfileUpdate


def get_profile_by_id(db: Session, profile_id: UUID) -> Optional[TrainerProfile]:
    """
    Retrieve a trainer profile by its ID.
    """
    return db.query(TrainerProfile).filter(TrainerProfile.id == profile_id).first()


def get_profile_by_user_id(db: Session, user_id: UUID) -> Optional[TrainerProfile]:
    """
    Retrieve a trainer profile by the trainer's user ID.
    """
    return db.query(TrainerProfile).filter(TrainerProfile.user_id == user_id).first()


def get_all_profiles(
    db: Session,
    skill_id: Optional[int] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[TrainerProfile]:
    """
    Retrieve all trainer profiles, supporting filters for city and skill.
    """
    query = (
        db.query(TrainerProfile)
        .join(User, TrainerProfile.user_id == User.id)
        .filter(
            User.account_status == AccountStatus.APPROVED.value,
            User.is_verified.is_(True),
        )
    )
    
    if skill_id is not None:
        query = query.filter(TrainerProfile.skill_id == skill_id)
        
    if city is not None:
        # Case-insensitive partial match for city names
        query = query.filter(TrainerProfile.city.ilike(f"%{city}%"))
        
    return query.offset(skip).limit(limit).all()


def create_trainer_profile(
    db: Session, user_id: UUID, profile_in: TrainerProfileCreate
) -> TrainerProfile:
    """
    Create a new trainer profile.
    """
    # 1. Verify user exists and is indeed a trainer
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    if user.role != UserRole.TRAINER.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only users with the 'trainer' role can have a trainer profile.",
        )

    # 2. Check if a profile already exists for this user
    existing_profile = get_profile_by_user_id(db, user_id=user_id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trainer profile already exists for this user. Use PUT/PATCH to update.",
        )

    # 3. Verify skill exists
    skill = db.query(Skill).filter(Skill.id == profile_in.skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )

    db_obj = TrainerProfile(
        user_id=user_id,
        skill_id=profile_in.skill_id,
        city=profile_in.city,
        experience_years=profile_in.experience_years,
        bio=profile_in.bio,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_trainer_profile(
    db: Session, user_id: UUID, profile_in: TrainerProfileUpdate
) -> TrainerProfile:
    """
    Update a trainer's profile.
    """
    profile = get_profile_by_user_id(db, user_id=user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer profile not found. Create one first.",
        )

    if profile_in.skill_id is not None:
        skill = db.query(Skill).filter(Skill.id == profile_in.skill_id).first()
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found.",
            )
        profile.skill_id = profile_in.skill_id

    if profile_in.city is not None:
        profile.city = profile_in.city

    if profile_in.experience_years is not None:
        profile.experience_years = profile_in.experience_years

    if profile_in.bio is not None:
        profile.bio = profile_in.bio

    db.commit()
    db.refresh(profile)
    return profile
