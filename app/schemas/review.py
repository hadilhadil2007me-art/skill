from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=1000)


class ReviewCreate(ReviewBase):
    trainer_id: UUID


class ReviewResponse(ReviewBase):
    id: UUID
    trainee_id: UUID
    trainer_id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ReviewDetailResponse(BaseModel):
    id: UUID
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    trainee: UserResponse

    model_config = {
        "from_attributes": True
    }
