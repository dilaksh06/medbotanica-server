# routers/users.py
from fastapi import APIRouter

app = APIRouter()  # <-- router, not FastAPI



@app.post("/user/register")
def register_user():
    return ("user registraions")


@app.get("/user/login")
def login_user():
    return ("user login")


@app.put("/user/update")
def update_user():
    return("update user")