from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# Assuming this model definition is correct
from models.caption import CaptionResponse 
from config.security import verify_token
# Import the utility function
from utils.test import generate_caption_from_path 
import shutil, uuid, os

router = APIRouter(prefix="/user", tags=["Predictions"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

UPLOAD_DIR = "uploads"
# Ensure the directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/predictions", response_model=CaptionResponse)
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

    # 1. Save the uploaded file temporarily
    filename = f"{uuid.uuid4()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    print(f"Saving uploaded file to {file_path}")
    try:
        # Write the file content to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # 2. 🧠 Call the BLIP model inference function
        # The utility loads the image from this path, generates the caption, and returns it.
        caption = generate_caption_from_path(file_path)

        # 3. Handle case where generation failed
        if "failed" in caption:
             raise HTTPException(status_code=500, detail=caption)

        return {
            "message": "Prediction successful",
            "user_id": user_id,
            "filename": filename,
            "caption": caption
        }

    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    
    finally:
        # 4. 🔥 IMPORTANT: Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleaned up temporary file: {file_path}")
