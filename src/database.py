from src.config import settings
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, text
from urllib.parse import urlparse

engine = create_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=280 
)

def create_db_and_tables():
    create_database_if_not_exists()
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def close_db_connection():
    engine.dispose()

def create_database_if_not_exists():
    url = urlparse(settings.DATABASE_URL)
    db_name = url.path[1:] 

    no_db_url = f"{url.scheme}://{url.username}:{url.password}@{url.hostname}:{url.port}"
    engine_no_db = create_engine(no_db_url, isolation_level="AUTOCOMMIT")

    with engine_no_db.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
        print(f"✅ Database '{db_name}' checked/created successfully.")

    engine_no_db.dispose()
