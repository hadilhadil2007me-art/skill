from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import RoleChecker, get_current_user
from app.database.session import get_db
from app.models.user import AccountStatus, User, UserRole
from app.schemas.user import UserApprovalUpdate, UserResponse
from app.services import user_service

router = APIRouter()
allow_admin = RoleChecker(allowed_roles=[UserRole.ADMIN.value])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user details",
    description="Retrieve the profile of the currently logged-in user.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List users",
    description="Admin-only list of registered users, optionally filtered by account status.",
)
def list_users(
    account_status: Optional[AccountStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin),
):
    query = db.query(User).order_by(User.created_at.desc())
    if account_status:
        query = query.filter(User.account_status == account_status.value)
    return query.all()


@router.patch(
    "/{user_id}/approval",
    response_model=UserResponse,
    summary="Approve or reject a user",
    description="Admin-only endpoint to approve, reject, or reset a user to pending.",
)
def update_user_approval(
    user_id: UUID,
    payload: UserApprovalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin),
):
    return user_service.update_account_status(
        db=db, user_id=str(user_id), account_status=payload.account_status
    )
