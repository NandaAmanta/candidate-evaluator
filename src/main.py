from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import create_db_and_tables, close_db_connection
from src.config import settings
from src.auth.router import router as auth_router
from src.candidate.router import router as candidate_router
from src.commons.exceptions import register_exception_handler
from fastapi_pagination import add_pagination
from src.vectordb import init_chroma
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Starting up...")
    create_db_and_tables()
    init_chroma()
    print("🔹 Startup complete.")
    yield
    close_db_connection()
    print("🔹 Shutting down...")
    
os.makedirs(settings.UPLOAD_DIR + "/cv", exist_ok=True)
os.makedirs(settings.UPLOAD_DIR + "/project", exist_ok=True)
app = FastAPI(
    title=settings.APP_NAME, 
    debug=settings.DEBUG, 
    lifespan=lifespan
)
app.include_router(auth_router, prefix='/api/v1')
app.include_router(candidate_router, prefix='/api/v1')
register_exception_handler(app)
add_pagination(app)
