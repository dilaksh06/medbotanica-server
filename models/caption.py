from pydantic import BaseModel

class CaptionResponse(BaseModel):
    message: str
    user_id: str
    filename: str
    caption: str
