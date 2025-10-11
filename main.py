from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.db import init_db_connection

# ✅ Import both routers
from routers.users import router as user_router
from routers.user_prediction import router as prediction_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_connection()
    yield


app = FastAPI(
    title="MedBotanica API",
    description="Herbal Plant Identification API",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ Include both routers
app.include_router(user_router)
app.include_router(prediction_router)


@app.get("/")
async def root():
    return {"message": "MedBotanica API is running 🚀"}
