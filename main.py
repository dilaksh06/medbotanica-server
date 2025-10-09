from fastapi import FastAPI
<<<<<<< HEAD
from contextlib import asynccontextmanager
from config.db import init_db_connection  # adjust path if needed
from routers.users import app as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # -------- Startup --------
    await init_db_connection()


    yield  # app runs here

    # -------- Shutdown --------
    # If you want to close DB connections, cleanup, etc.
    # client.close()

# Pass lifespan into FastAPI
app = FastAPI(lifespan=lifespan)

# Include the user router
app.include_router(user_router)

# Example route
@app.get("/")
async def root():
    return {"message": "MedBotanica API is running 🚀"}
=======
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
>>>>>>> b820f8c4899df31aa38e9d8a487fd99c89b5a4de
