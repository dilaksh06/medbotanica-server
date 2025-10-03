from fastapi import FastAPI
from beanie import init_beanie
import motor.motor_asyncio
from models.users import User
from models.prediction import Prediction
from routers import prediction, users

app = FastAPI(title="Herbal Plant Captioning API")

@app.on_event("startup")
async def app_init():
    # connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.herbal_db   # database name

    # init Beanie with your models
    await init_beanie(database=db, document_models=[User, Prediction])

# Routers
app.include_router(users.app)
app.include_router(prediction.router)
