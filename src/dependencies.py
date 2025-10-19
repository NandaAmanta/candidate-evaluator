from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_session
from src.auth.repositories.user_repository import UserRepository,UserRepositoryProtocol

def get_user_repository(session: Session = Depends(get_session)) -> UserRepositoryProtocol:
    return UserRepository(session)

