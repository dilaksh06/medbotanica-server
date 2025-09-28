from fastapi import FastAPI, Depends, HTTPException, status

app=FastAPI()




@app.get("/user/login")
def login_user():
    return ("user login")

@app.post("/user/register")
def register_user():
    return ("user registraions")

@app.put("/user/update")
def update_user():
    return("update user")
