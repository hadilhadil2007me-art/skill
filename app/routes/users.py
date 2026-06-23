from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user details",
    description="Retrieve the profile of the currently logged-in user.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
