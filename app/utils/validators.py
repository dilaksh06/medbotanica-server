# app/utils/validators.py
import re
from fastapi import HTTPException, UploadFile
from typing import List, Optional
from app.models.user import User

# Allowed file extensions (can extend this list)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 5  # Maximum allowed file size


# ------------------- User Validations ------------------- #
async def ensure_unique_email(email: str):
    """
    Check if the email is already registered in the database.
    Raises HTTPException if email exists.
    """
    existing = await User.find_one(User.email == email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")


def validate_email(email: str):
    """
    Validate email format using regex.
    Raises HTTPException if invalid.
    """
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")


def validate_password(password: str):
    """
    Validate password strength:
    - Minimum 8 characters
    - Must contain uppercase, lowercase, digit, and special character
    Raises HTTPException if invalid.
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must include an uppercase letter")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must include a lowercase letter")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must include a number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Password must include a special character")


def validate_phone_number(phone: str):
    """
    Validate phone number format: +1234567890 or 10-15 digits.
    """
    phone_regex = r"^\+?\d{10,15}$"
    if not re.match(phone_regex, phone):
        raise HTTPException(status_code=400, detail="Invalid phone number format")


# ------------------- File Validations ------------------- #
def validate_file_type(filename: str, allowed_extensions: Optional[List[str]] = None):
    """
    Validate file extension.
    Raises HTTPException if not allowed.
    """
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS

    ext = filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )


async def validate_file_size(file: UploadFile, max_size_mb: int = MAX_FILE_SIZE_MB):
    """
    Validate uploaded file size.
    Raises HTTPException if file is too large.
    """
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    await file.seek(0)  # reset read pointer for further processing
    if size_mb > max_size_mb:
        raise HTTPException(status_code=400, detail=f"File size exceeds {max_size_mb} MB")


async def validate_uploaded_file(file: UploadFile, allowed_extensions: Optional[List[str]] = None, max_size_mb: int = MAX_FILE_SIZE_MB):
    """
    Validate uploaded file object: type and size.
    """
    validate_file_type(file.filename, allowed_extensions)
    await validate_file_size(file, max_size_mb)
