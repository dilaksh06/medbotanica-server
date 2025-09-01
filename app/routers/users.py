from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserOut, User
from app.dependencies import get_current_user
from typing import Optional

# Create a new router for user-related endpoints
router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/me", response_model=UserOut)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current authenticated user's profile.
    
    This endpoint requires a valid JWT access token. It uses the token to
    retrieve the user's details from the database and returns them.
    """
    # The get_current_user dependency already handles authentication and
    # fetching the user object. We can directly return the user's data.
    return UserOut(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        profile_url=current_user.profile_url,
        role=current_user.role,
        created_at=current_user.created_at,
    )
