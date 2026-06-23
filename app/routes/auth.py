from datetime import timedelta
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.database.session import get_db
from app.schemas.user import (
    UserCreate,
    UserRegistrationResponse,
    UserResponse,
    UserVerificationRequest,
    Token,
)
from app.services import user_service

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a user on the SkillUp platform as an Admin, Trainer, or Trainee.",
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db=db, user_in=user_in)
    return {
        "user": user,
        "verification_code": user.verification_code,
        "message": (
            "Account created. Verify your account, then wait for admin approval."
        ),
    }


@router.post(
    "/verify",
    response_model=UserResponse,
    summary="Verify a new account",
    description="Verifies a newly created account using the code sent to the user.",
)
def verify_account(payload: UserVerificationRequest, db: Session = Depends(get_db)):
    return user_service.verify_user(db=db, email=payload.email, code=payload.code)


@router.post(
    "/login",
    response_model=Token,
    summary="User Login",
    description="Authenticate email and password to receive a JWT access token for role-restricted operations.",
)
def login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Map form fields from OAuth2 request
    from app.schemas.user import UserLogin
    credentials = UserLogin(email=form_data.username, password=form_data.password)

    # Authenticate user
    user = user_service.authenticate_user(db=db, credentials=credentials)

    # Create access token
    access_token = security.create_access_token(subject=user.id)

    # Set HttpOnly cookie for session-based auth (safer than localStorage)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.PRODUCTION,  # enable secure cookies in production (with HTTPS)
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
