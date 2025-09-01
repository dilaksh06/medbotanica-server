# app/routers/detections.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from pydantic import BaseModel
from jose import jwt
from datetime import datetime

from app.models.detection import Detection
from app.core.config import settings

router = APIRouter(prefix="/detections", tags=["detections"])
auth_scheme = HTTPBearer()


# ------------------- Response Models ------------------- #
class DetectionOut(BaseModel):
    id: str
    image_url: str
    result: str
    created_at: datetime  # proper datetime type


# ------------------- Auth Helper ------------------- #
def get_user_id_from_token(token: HTTPAuthorizationCredentials) -> str:
    """
    Decode JWT and return user ID (sub).
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


# ------------------- Routes ------------------- #
@router.get("/", response_model=List[DetectionOut])
async def list_detections(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Get all detections for the logged-in user.
    """
    user_id = get_user_id_from_token(token)
    try:
        detections = await Detection.find(Detection.user_id == user_id).to_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch detections: {str(e)}")

    return [
        DetectionOut(
            id=str(det.id),
            image_url=det.image_url,
            result=det.result,
            created_at=det.created_at
        )
        for det in detections
    ]


@router.get("/{detection_id}", response_model=DetectionOut)
async def get_detection(
    detection_id: str,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """
    Get a single detection by ID.
    """
    user_id = get_user_id_from_token(token)
    try:
        det = await Detection.get(detection_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch detection: {str(e)}")

    if not det or det.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detection not found")

    return DetectionOut(
        id=str(det.id),
        image_url=det.image_url,
        result=det.result,
        created_at=det.created_at
    )
