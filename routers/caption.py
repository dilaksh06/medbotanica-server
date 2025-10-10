from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.caption import CaptionResponse
from config.security import verify_token
import shutil, uuid, os

router = APIRouter(prefix="/user", tags=["Predictions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/prediction", response_model=CaptionResponse)
async def get_caption(
    image: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing user ID")

    filename = f"{uuid.uuid4()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # 🧠 Replace with actual ML model inference
    caption = f"This is a generated caption for {filename}"

    return {
        "message": "Prediction successful",
        "user_id": user_id,
        "filename": filename,
        "caption": caption
    }
