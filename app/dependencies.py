from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Annotated

# Import the settings object directly to access configuration values
from app.core.config import settings
from app.models.user import User

# This utility will handle token extraction from the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class TokenData(BaseModel):
    user_id: str | None = None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the current authenticated user from the JWT token.
    
    This function decodes the JWT token, extracts the user ID, and fetches
    the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = await User.get(token_data.user_id)
    if user is None:
        raise credentials_exception
        
    return user
