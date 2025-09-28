from datetime import datetime


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
