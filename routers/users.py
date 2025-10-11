# routers/users.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from models.users import User, LoginUser, RegisterUser, UpdateUser, UserOut
from config.security import verify_password, hash_password, create_access_token
from utils.validators import (
    validate_email,
    validate_password,
    ensure_unique_email,
    validate_phone_number,
)

app = APIRouter()


# Request Models
class LoginRequest(BaseModel):
    email: str
    password: str


# Response Models
class LoginData(BaseModel):
    user: UserOut
    token: str


class LoginSuccessResponse(BaseModel):
    success: bool
    message: str
    data: LoginData


# -------- ROUTES --------

@app.post("/user/register", response_model=LoginSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterUser):
    validate_email(payload.email)

    if len(payload.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long. Maximum 72 bytes allowed."
        )

    if getattr(payload, "phone", None):
        validate_phone_number(payload.phone)

    await ensure_unique_email(payload.email)

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        phone=getattr(payload, "phone", None)
    )
    await user.insert()

    # Create JWT token for immediate login
    token = create_access_token(subject=str(user.id))

    user_out = UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )

    return LoginSuccessResponse(
        success=True,
        message="Registration successful",
        data={
            "user": user_out,
            "token": token
        }
    )


@app.post("/user/login", response_model=LoginSuccessResponse, status_code=status.HTTP_202_ACCEPTED)
async def login_user(payload: LoginRequest):
    user = await User.find_one(User.email == payload.email)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(subject=str(user.id))

    user_out = UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )

    return LoginSuccessResponse(
        success=True,
        message="Login successful",
        data={
            "user": user_out,
            "token": token
        }
    )


@app.put("/user/update")
def update_user():
    return "update user"
