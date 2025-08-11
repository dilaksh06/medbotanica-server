from beanie import Document
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime

class User(Document):
    name: str
    email: EmailStr
    hashed_password: str
    profile_url: str | None = None
    role: Literal["contributor", "user"] = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["contributor", "user"] = "user"

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    profile_url: str | None
    role: str
    created_at: datetime
