from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.storage import save_file
from app.services.ml import predict_image
from app.models.detection import Detection
from app.core.config import settings
from jose import jwt
from app.core.config import settings

router = APIRouter(prefix="/predict", tags=["predict"])
auth_scheme = HTTPBearer()

def get_user_id_from_token(token: HTTPAuthorizationCredentials):
    try:
        payload = jwt.decode(token.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
async def predict(file: UploadFile = File(...), token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    user_id = get_user_id_from_token(token)
    # save file (local or s3)
    saved_url = await save_file(file)
    # call ML predict (placeholder)
    result = await predict_image(saved_url)
    # save detection record
    det = Detection(user_id=user_id, image_url=saved_url, result=result)
    await det.insert()
    return {"result": result, "image_url": saved_url}
