from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import create_db_and_tables, close_db_connection
from src.config import settings
from src.auth.router import router as auth_router
from src.core.exceptions import register_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Starting up...")
    create_db_and_tables()
    yield
    close_db_connection()
    print("🔹 Shutting down...")

app = FastAPI(
    title=settings.APP_NAME, 
    debug=settings.DEBUG, 
    lifespan=lifespan
)

app.include_router(auth_router, prefix='/api/v1')
register_exception_handler(app)