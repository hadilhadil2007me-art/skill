from typing import Optional
from pydantic import BaseModel, Field


class SkillBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)


class SkillResponse(SkillBase):
    id: int

    model_config = {
        "from_attributes": True
    }
