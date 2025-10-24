from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "FastAPI CRUD with SQLModel")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 60 * 60 * 24))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 60 * 60 * 24 * 7))
    JWT_ACCESS_TOKEN_SECRET_KEY = os.getenv("JWT_ACCESS_TOKEN_SECRET_KEY")
    JWT_REFRESH_TOKEN_SECRET_KEY = os.getenv("JWT_REFRESH_TOKEN_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "storage")
    LLM_CLIENT_API_TOKEN = os.getenv("LLM_CLIENT_API_TOKEN", "sk-")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openrouter.ai")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "coh-key")
    CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH", "chroma_data")
settings = Settings()