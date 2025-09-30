from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Prediction
from schemas import PredictionResponse
from ml.caption_model import generate_caption
import shutil, os, uuid

router = APIRouter(prefix="/user", tags=["Predictions"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/prediction", response_model=PredictionResponse)
def create_prediction(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    #  Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Save uploaded image
    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Generate caption using ML model (BLIP-2 / dummy for now)
    caption = generate_caption(file_path)

    
    prediction = Prediction(image_path=file_path, caption=caption, owner=user)
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction