from typing import List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import TokenData

# OAuth2 for explicit Authorization header flows (still supported)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False,
)


def _decode_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(id=user_id)
    except InvalidTokenError:
        raise credentials_exception


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> User:
    """
    Resolve the current user from either the Authorization header (Bearer)
    or from a secure HttpOnly cookie named `access_token`.
    """
    access_token = None

    # 1) Prefer Authorization header (OAuth2 flow)
    if token:
        access_token = token
    # 2) Fall back to cookie (HttpOnly cookie set by login endpoint)
    if not access_token:
        access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = _decode_token(access_token)

    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


class RoleChecker:
    """
    A dependency class used to enforce role-based permissions.
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user
