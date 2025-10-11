from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Prediction(Document):
    image_path: str
    caption: str
    plant_name: Optional[str] = None
    scientific_name: Optional[str] = None
    confidence: Optional[float] = None
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "predictions"
