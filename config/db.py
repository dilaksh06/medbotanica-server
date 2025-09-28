from motor.motor_asyncio import AsyncIOMotorClient

from  core.config import settings
from beanie import init_beanie
from models.users import User
client=None

async def init_db_connection():
    global client
    client=AsyncIOMotorClient(settings.mongodb_uri)
    db=client[settings.mongo_dbname]
    await init_beanie(database=db,document_models=[User])
