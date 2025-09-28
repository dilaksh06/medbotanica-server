from datetime import datetime
from beanie import Document
from pydantic import BaseModel, EmailStr,Field
from typing import Literal

class User(Document):
    name: str
    email: EmailStr
    hashed_password: str
    profile_url: str | None = None
    role: Literal["contributor", "user"] = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class Login_user:
    name:str
    email:str
    password:str

class Register_user:
    name:str
    email:str
    hashed_password:str
    created_at:datetime.now
    profile_url:str

class Update_user:
    name:str
    hashed_password:str
    created_at: datetime
