from fastapi import APIRouter, HTTPException, status
from app.models.user import User, UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResp(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate):
    existing = await User.find_one(User.email == payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
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

@router.post("/login", response_model=TokenResp)
async def login(payload: LoginRequest):
    user = await User.find_one(User.email == payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return TokenResp(access_token=token)
