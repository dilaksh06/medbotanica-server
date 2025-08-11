from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson import ObjectId

class Detection(Document):
    user_id: str
    image_url: str
    result: dict   # can store label, confidence, caption etc.
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "detections"

class DetectionCreate(BaseModel):
    user_id: str
    image_url: str
    result: dict
