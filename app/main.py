# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routers import auth, predict, detections
from app.core.config import settings

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
