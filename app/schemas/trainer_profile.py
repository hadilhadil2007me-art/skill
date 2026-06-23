from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse
from app.schemas.skill import SkillResponse


class TrainerProfileBase(BaseModel):
    city: str = Field(..., min_length=2, max_length=50)
    experience_years: int = Field(default=0, ge=0, le=60)
    bio: Optional[str] = Field(default=None, max_length=1000)


class TrainerProfileCreate(TrainerProfileBase):
    skill_id: int


class TrainerProfileUpdate(BaseModel):
    skill_id: Optional[int] = None
    city: Optional[str] = Field(default=None, min_length=2, max_length=50)
    experience_years: Optional[int] = Field(default=None, ge=0, le=60)
    bio: Optional[str] = Field(default=None, max_length=1000)


class TrainerProfileResponse(TrainerProfileBase):
    id: UUID
    user_id: UUID
    skill_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


# Detailed response with nested user and skill objects
class TrainerProfileDetailResponse(BaseModel):
    id: UUID
    city: str
    experience_years: int
    bio: Optional[str] = None
    user: UserResponse
    skill: Optional[SkillResponse] = None

    model_config = {
        "from_attributes": True
    }
