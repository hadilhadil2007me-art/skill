from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


def get_skill_by_id(db: Session, skill_id: int) -> Optional[Skill]:
    """
    Retrieve a skill by its ID.
    """
    return db.query(Skill).filter(Skill.id == skill_id).first()


def get_skill_by_name(db: Session, name: str) -> Optional[Skill]:
    """
    Retrieve a skill by its name.
    """
    return db.query(Skill).filter(Skill.name.ilike(name)).first()


def get_skills(db: Session, skip: int = 0, limit: int = 100) -> List[Skill]:
    """
    Get a list of skills with pagination.
    """
    return db.query(Skill).offset(skip).limit(limit).all()


def create_skill(db: Session, skill_in: SkillCreate) -> Skill:
    """
    Create a new skill in the catalog.
    """
    existing_skill = get_skill_by_name(db, name=skill_in.name)
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A skill with this name already exists.",
        )
    
    db_obj = Skill(
        name=skill_in.name,
        description=skill_in.description,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_skill(db: Session, skill_id: int, skill_in: SkillUpdate) -> Skill:
    """
    Update an existing skill.
    """
    skill = get_skill_by_id(db, skill_id=skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )
    
    # Check if updated name conflicts with another skill
    if skill_in.name and skill_in.name != skill.name:
        existing_skill = get_skill_by_name(db, name=skill_in.name)
        if existing_skill:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A skill with this name already exists.",
            )
        skill.name = skill_in.name
        
    if skill_in.description is not None:
        skill.description = skill_in.description

    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill_id: int) -> Skill:
    """
    Delete a skill from the catalog.
    """
    skill = get_skill_by_id(db, skill_id=skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )
    db.delete(skill)
    db.commit()
    return skill
