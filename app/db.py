from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.detection import Detection
import asyncio
from app.core.config import settings

client = None

async def init_db():
    global client
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongo_dbname]
    # initialize beanie with document models
    await init_beanie(database=db, document_models=[User, Detection])
