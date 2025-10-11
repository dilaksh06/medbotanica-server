from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from models.users import User
from models.prediction import Prediction
from utils.validators import validate_uploaded_file
from app.ml.caption_model import generate_caption
import os, uuid, shutil

router = APIRouter(prefix="/user", tags=["Predictions"])

UPLOAD_DIR = "uploads/herbal_plants"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/prediction")
async def create_prediction(user_id: str, file: UploadFile = File(...)):
    """
    Create a herbal plant prediction from an uploaded image.
    """

    # 1. Check if user exists
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Validate file (type + size)
    await validate_uploaded_file(file)

    # 3. Save uploaded image with unique name
    file_ext = os.path.splitext(file.filename)[-1] or ".jpg"
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Generate herbal caption using ML model
    caption, plant_name, scientific_name, confidence = generate_caption(file_path)

    # 5. Save prediction in MongoDB
    prediction = Prediction(
        image_path=file_path,
        caption=caption,
        plant_name=plant_name,
        scientific_name=scientific_name,
        confidence=confidence,
        user_id=str(user.id),
    )
    await prediction.insert()

    return {
        "id": str(prediction.id),
        "user_id": str(user.id),
        "caption": caption,
        "plant_name": plant_name,
        "scientific_name": scientific_name,
        "confidence": confidence,
        "image_path": file_path,
        "created_at": prediction.created_at,
    }
