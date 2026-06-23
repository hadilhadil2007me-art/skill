from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.training_request import RequestStatus
from app.schemas.user import UserResponse


class TrainingRequestBase(BaseModel):
    message: Optional[str] = Field(default=None, max_length=1000)


class TrainingRequestCreate(TrainingRequestBase):
    trainer_id: UUID


class TrainingRequestUpdate(BaseModel):
    status: RequestStatus


class TrainingRequestResponse(TrainingRequestBase):
    id: UUID
    trainee_id: UUID
    trainer_id: UUID
    status: RequestStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TrainingRequestDetailResponse(BaseModel):
    id: UUID
    message: Optional[str] = None
    status: RequestStatus
    created_at: datetime
    trainee: UserResponse
    trainer: UserResponse

    model_config = {
        "from_attributes": True
    }
