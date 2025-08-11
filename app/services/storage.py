import os
from fastapi import UploadFile
from uuid import uuid4
from app.core.config import settings
import aiofiles
import boto3
from botocore.exceptions import BotoCoreError

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file_local(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename)[1]
    fname = f"{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    async with aiofiles.open(path, "wb") as out_file:
        content = await file.read()  # async
        await out_file.write(content)
    # return a path or static server URL for production
    return path

async def save_file_s3(file: UploadFile) -> str:
    s3 = boto3.client("s3")
    key = f"uploads/{uuid4().hex}_{file.filename}"
    try:
        s3.upload_fileobj(file.file, settings.s3_bucket, key)
        return f"https://{settings.s3_bucket}.s3.amazonaws.com/{key}"
    except BotoCoreError as e:
        raise

async def save_file(file: UploadFile) -> str:
    if settings.s3_bucket:
        return await save_file_s3(file)
    return await save_file_local(file)
