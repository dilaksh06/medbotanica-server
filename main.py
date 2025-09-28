from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.db import init_db_connection  # adjust path if needed
from routers.users import app as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # -------- Startup --------
    await init_db_connection()


    yield  # app runs here

    # -------- Shutdown --------
    # If you want to close DB connections, cleanup, etc.
    # client.close()

# Pass lifespan into FastAPI
app = FastAPI(lifespan=lifespan)

# Include the user router
app.include_router(user_router)

# Example route
@app.get("/")
async def root():
    return {"message": "MedBotanica API is running 🚀"}
