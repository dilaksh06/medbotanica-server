from fastapi import FastAPI
from app.db import init_db
from app.routers import auth, predict
from app.core.config import settings
import asyncio

app = FastAPI(title="MedBotanica Server")

app.include_router(auth.router)
app.include_router(predict.router)

@app.on_event("startup")
async def startup_event():
    await init_db()
    # optionally load model: from app.services.ml import load_model; await load_model()

@app.get("/")
def root():
    return {"msg": "MedBotanica API running"}
