# app/routers/predict.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from jose import jwt

from app.services.storage import save_file
from app.services.ml import predict_image
from app.models.detection import Detection
from app.core.config import settings
from app.utils.validators import validate_uploaded_file  # make sure path is correct

router = APIRouter(prefix="/predict", tags=["predict"])
auth_scheme = HTTPBearer()


# ------------------- Response Model ------------------- #
class PredictOut(BaseModel):
    result: str
    image_url: str


# ------------------- Auth Helper ------------------- #
def get_user_id_from_token(token: HTTPAuthorizationCredentials) -> str:
    """
    Decode JWT and extract user ID. Raises 401 if invalid.
    """
    try:
        payload = jwt.decode(
            token.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )


# ------------------- Route ------------------- #
@router.post("/", response_model=PredictOut, status_code=status.HTTP_201_CREATED)
async def predict(
    file: UploadFile = File(...),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """
    Upload an image, run ML prediction, save detection record, and return result.
    """
    # Validate uploaded file
    await validate_uploaded_file(file)

    # Get user ID from JWT
    user_id = get_user_id_from_token(token)

    # Save file (local or S3)
    try:
        saved_url = await save_file(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File saving failed: {str(e)}")

    # Call ML prediction
    try:
        result = await predict_image(saved_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # Save detection record
    try:
        detection = Detection(user_id=user_id, image_url=saved_url, result=result)
        await detection.insert()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save detection: {str(e)}")

    # Return standardized response
    return PredictOut(result=result, image_url=saved_url)
