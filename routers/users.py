# routers/users.py
from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from typing import Optional

from models.users import User,LoginUser,RegisterUser,UpdateUser,UserOut

from config.security import verify_password,hash_password,create_access_token
from utils.validators import validate_email,validate_password,ensure_unique_email,validate_phone_number


app = APIRouter()  # <-- router, not FastAPI

# Request Models
class LoginReq(BaseModel):
    email:str
    password:str

# Response Models
class LoginData(BaseModel):
    user:User
    token:str

# full login response model

class LoginSuccessResponse(BaseModel):
    success:bool
    message:str
    data:LoginData


#------ROutes------------

@app.post("/user/register",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def register_user(payload:RegisterUser):
    
    validate_email(payload.email)
    # Add this check
    if len(payload.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long. Maximum 72 bytes allowed."
        )
    if getattr(payload,"phone",None):
        validate_phone_number(payload.phone)
    await ensure_unique_email(payload.email)

    user=User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        phone=getattr(payload,"phone",None)
    )
    await user.insert()


    return UserOut(
        id=str(user.id),
        name=user.name,
        email=user.email,
        created_at=user.created_at,
    )






@app.get("/user/login")
def login_user():
    return ("user login")


@app.put("/user/update")
def update_user():
    return("update user")