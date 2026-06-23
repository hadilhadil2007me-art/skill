from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import RoleChecker
from app.database.session import get_db
from app.models.user import UserRole
from app.schemas.skill import SkillCreate, SkillResponse, SkillUpdate
from app.services import skill_service

router = APIRouter()

# Dependency for checking Admin permissions
allow_admin = RoleChecker(allowed_roles=[UserRole.ADMIN.value])


@router.get(
    "/",
    response_model=List[SkillResponse],
    summary="List all skills",
    description="Retrieve a paginated list of all available training domains.",
)
def read_skills(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    return skill_service.get_skills(db=db, skip=skip, limit=limit)


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get skill by ID",
    description="Retrieve specific details of a skill by its ID.",
)
def read_skill(skill_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    skill = skill_service.get_skill_by_id(db=db, skill_id=skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )
    return skill


@router.post(
    "/",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new skill",
    description="Allows administrators to add new skills to the catalog.",
    dependencies=[Depends(allow_admin)],
)
def create_new_skill(skill_in: SkillCreate, db: Session = Depends(get_db)):
    return skill_service.create_skill(db=db, skill_in=skill_in)


@router.put(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update a skill",
    description="Allows administrators to modify an existing skill's details.",
    dependencies=[Depends(allow_admin)],
)
def update_existing_skill(
    skill_id: int, skill_in: SkillUpdate, db: Session = Depends(get_db)
):
    return skill_service.update_skill(
        db=db, skill_id=skill_id, skill_in=skill_in
    )


@router.delete(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Delete a skill",
    description="Allows administrators to delete a skill from the database catalog.",
    dependencies=[Depends(allow_admin)],
)
def delete_existing_skill(skill_id: int, db: Session = Depends(get_db)):
    return skill_service.delete_skill(db=db, skill_id=skill_id)
