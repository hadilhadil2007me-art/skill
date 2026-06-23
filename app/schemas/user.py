from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.TRAINEE
    phone: Optional[str] = Field(default=None, pattern=r"^\+?[0-9\s\-]{8,20}$")


# Properties to receive on user creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=40)


# Properties to receive on user update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    password: Optional[str] = Field(default=None, min_length=6, max_length=40)
    phone: Optional[str] = Field(default=None, pattern=r"^\+?[0-9\s\-]{8,20}$")


# Properties to return in API response
class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True  # Enable compatibility with SQLAlchemy models
    }


# Login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token representation
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Data stored in JWT payload
class TokenData(BaseModel):
    id: Optional[str] = None
