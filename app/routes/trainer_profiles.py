from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, RoleChecker
from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.trainer_profile import (
    TrainerProfileCreate,
    TrainerProfileUpdate,
    TrainerProfileResponse,
    TrainerProfileDetailResponse,
)
from app.services import trainer_service

router = APIRouter()

# Dependency for trainer operations
allow_trainer = RoleChecker(allowed_roles=[UserRole.TRAINER.value])


@router.get(
    "/",
    response_model=List[TrainerProfileDetailResponse],
    summary="Search & list trainers",
    description="Retrieve all trainer profiles. Filter results by specific skills and Algerian cities.",
)
def read_trainers(
    skill_id: Optional[int] = None,
    city: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return trainer_service.get_all_profiles(
        db=db, skill_id=skill_id, city=city, skip=skip, limit=limit
    )


@router.get(
    "/me",
    response_model=TrainerProfileDetailResponse,
    summary="Get my trainer profile",
    description="Retrieves the profile of the currently logged-in trainer.",
    dependencies=[Depends(allow_trainer)],
)
def read_my_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    profile = trainer_service.get_profile_by_user_id(
        db=db, user_id=current_user.id
    )
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't created a trainer profile yet.",
        )
    return profile


@router.get(
    "/{profile_id}",
    response_model=TrainerProfileDetailResponse,
    summary="Get trainer profile by ID",
    description="Retrieve detailed information about a trainer, including skill and contact info.",
)
def read_trainer(profile_id: UUID, db: Session = Depends(get_db)):
    profile = trainer_service.get_profile_by_id(db=db, profile_id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trainer profile not found.",
        )
    return profile


@router.post(
    "/me",
    response_model=TrainerProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create trainer profile",
    description="Creates a profile for the logged-in trainer. (Required to become discoverable).",
)
def create_my_profile(
    profile_in: TrainerProfileCreate,
    current_user: User = Depends(allow_trainer),
    db: Session = Depends(get_db),
):
    return trainer_service.create_trainer_profile(
        db=db, user_id=current_user.id, profile_in=profile_in
    )


@router.put(
    "/me",
    response_model=TrainerProfileResponse,
    summary="Update trainer profile",
    description="Updates the profile of the logged-in trainer.",
)
def update_my_profile(
    profile_in: TrainerProfileUpdate,
    current_user: User = Depends(allow_trainer),
    db: Session = Depends(get_db),
):
    return trainer_service.update_trainer_profile(
        db=db, user_id=current_user.id, profile_in=profile_in
    )
