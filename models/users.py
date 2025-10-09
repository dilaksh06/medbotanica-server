from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from beanie import Document


class User(Document):
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
  
# ---------------- Request Models ----------------
class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    hashed_password: Optional[str] = None
    created_at: Optional[datetime] = None

# ---------------- Response Model ----------------
class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
