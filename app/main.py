from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from app.db import init_db
from app.routers import auth, predict, detections
from app.core.config import settings
from app.models.user import User
from app.dependencies import get_current_user

# ------------------- App Initialization ------------------- #
app = FastAPI(
    title="MedBotanica Server",
    description="Backend API for MedBotanica mobile and web applications",
    version="1.0.0",
)

# ------------------- CORS Middleware ------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Routers ------------------- #
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(predict.router, prefix="/predict", tags=["predict"])
app.include_router(detections.router, prefix="/detections", tags=["detections"])

# ------------------- Startup Event ------------------- #
@app.on_event("startup")
async def startup_event():
    """
    Initialize database and optionally preload ML models.
    """
    await init_db()
    # Optionally preload ML model
    # from app.services.ml import load_model
    # await load_model()

# ------------------- Root Endpoint ------------------- #
@app.get("/", summary="Root endpoint")
def root():
    """
    Simple health check endpoint.
    """
    return {"msg": "MedBotanica API running"}

# ------------------- New User Endpoint ------------------- #
# This new endpoint uses the `get_current_user` dependency to protect the route.
# A valid JWT token is required to access this endpoint, and it returns the
# details of the authenticated user.
@app.get("/users/me", response_model=User, summary="Get current user")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieve the current authenticated user's information.
    """
    return current_user
