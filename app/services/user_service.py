import secrets
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import AccountStatus, User, UserRole
from app.schemas.user import UserCreate, UserLogin


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user from the database by email address.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieve a user from the database by their unique ID.
    """
    try:
        parsed_id = user_id if isinstance(user_id, UUID) else UUID(str(user_id))
    except ValueError:
        return None
    return db.query(User).filter(User.id == parsed_id).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Register a new user in the platform, hashing their password.
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    
    verification_code = f"{secrets.randbelow(900000) + 100000}"

    db_obj = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role.value,
        phone=user_in.phone,
        wilaya=user_in.wilaya,
        profession=user_in.profession,
        account_status=(
            AccountStatus.APPROVED.value
            if user_in.role == UserRole.ADMIN
            else AccountStatus.PENDING.value
        ),
        is_verified=user_in.role == UserRole.ADMIN,
        verification_code=None if user_in.role == UserRole.ADMIN else verification_code,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def verify_user(db: Session, email: str, code: str) -> User:
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    if user.is_verified:
        return user
    if not user.verification_code or user.verification_code != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code.",
        )
    user.is_verified = True
    user.verification_code = None
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_account_status(db: Session, user_id: str, account_status: AccountStatus) -> User:
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    user.account_status = account_status.value
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, credentials: UserLogin) -> User:
    """
    Authenticate a user by verifying their email and password.
    """
    user = get_user_by_email(db, email=credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your account before logging in.",
        )
    if user.account_status != AccountStatus.APPROVED.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is waiting for admin approval.",
        )
    return user
