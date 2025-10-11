from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from models.users import User, LoginUser, RegisterUser, UpdateUser, UserOut
from config.security import verify_password, hash_password, create_access_token
from utils.validators import validate_email, validate_password, ensure_unique_email, validate_phone_number

router = APIRouter(prefix="/user", tags=["Users"])  # ✅ one router only


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


# ------ ROUTES ------------

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterUser):
    validate_email(payload.email)
    if len(payload.password.encode('utf-8')) > 72:
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
        phone=getattr(payload, "phone", None),
    )
    await user.insert()

    return UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )


@router.post("/login", response_model=LoginSuccessResponse, status_code=status.HTTP_202_ACCEPTED)
async def login_user(payload: LoginRequest):
    user = await User.find_one(User.email == payload.email)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

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
        data=LoginData(user=user_out, token=token)
    )


@router.put("/update")
async def update_user():
    return {"message": "update user"}
