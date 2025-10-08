import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt
from jose import JWTError

# It's a good practice to import settings to centralize configuration
from core.config import settings

# Initialize a context for password hashing with the bcrypt algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a plain password using the configured CryptContext.
    
    Args:
        password: The plaintext password string to be hashed.
    Returns:
        The hashed password string.
    """
    # Bcrypt has a 72-byte limit, so we truncate if necessary
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='ignore')
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password.
    
    Args:
        plain_password: The plaintext password string to verify.
        hashed_password: The hashed password string from the database.
        
    Returns:
        True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: Optional[int] = None) -> str:
    """
    Creates a JWT access token for a given subject (e.g., a user ID).
    
    Args:
        subject: The data to be encoded in the JWT's 'sub' claim.
        expires_delta: Optional time in minutes for the token to expire. 
                       Defaults to the value in settings if not provided.

    Returns:
        The encoded JWT as a string.
    """
    # Use the expiration time from settings if not explicitly provided
    if expires_delta is None:
        expires_delta = settings.jwt_exp_minutes

    to_encode = {"sub": str(subject)}
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt



def verify_token(token: str) -> Optional[dict]:
    """
    Verifies and decodes a JWT access token.

    Args:
        token: The JWT string sent by the client.

    Returns:
        The decoded payload (e.g., {'sub': 'user_id'}) if valid.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token expired
        return None
    except JWTError:
        # Invalid token
        return None
