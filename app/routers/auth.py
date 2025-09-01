from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from app.models.user import User, UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.validators import validate_email, validate_password, ensure_unique_email, validate_phone_number

# Removed the prefix here, as it's already set in main.py
router = APIRouter(tags=["auth"])


# ------------------- Request Models ------------------- #
class LoginRequest(BaseModel):
    email: str
    password: str


# ------------------- Response Models ------------------- #
# Define the data part of the login response
class LoginData(BaseModel):
    user: UserOut
    token: str

# Define the full login success response model to match the frontend's expectations
class LoginSuccessResponse(BaseModel):
    success: bool
    message: str
    data: LoginData

# The original token response model is no longer needed for a successful login
# class TokenResp(BaseModel):
#     access_token: str
#     token_type: str = "bearer"


# ------------------- Routes ------------------- #
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate):
    """
    Register a new user after validating email, password, and optional phone number.
    """
    # Validate inputs
    validate_email(payload.email)
    validate_password(payload.password)
    if getattr(payload, "phone", None):  # optional phone field
        validate_phone_number(payload.phone)
    await ensure_unique_email(payload.email)

    # Create and insert user
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
        phone=getattr(payload, "phone", None)
    )
    await user.insert()

    return UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        profile_url=user.profile_url,
        role=user.role,
        created_at=user.created_at,
    )


@router.post("/login", response_model=LoginSuccessResponse)
async def login(payload: LoginRequest):
    """
    Authenticate user and return a comprehensive response with user data and JWT token.
    """
    # Find the user by email
    user = await User.find_one(User.email == payload.email)

    # Verify user existence and password.
    # The `and` operator ensures `user` is not None before attempting to access its properties.
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create a JWT token for the authenticated user
    token = create_access_token(subject=str(user.id))

    # Construct the UserOut model for the response
    user_out = UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        profile_url=user.profile_url,
        role=user.role,
        created_at=user.created_at,
    )

    # Return the structured response that the frontend expects
    return LoginSuccessResponse(
        success=True,
        message="Login successful",
        data={
            "user": user_out,
            "token": token
        }
    )
