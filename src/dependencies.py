from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database import get_session
from src.auth.utils.jwt import decode_access_token
from src.config import settings
from jwt.exceptions import InvalidTokenError
from src.auth.repositories.user_repository import UserRepository,UserRepositoryProtocol
from src.candidate.repositories.candidate_repository import CandidateRepository, CandidateRepositoryProtocol

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  # endpoint login

def get_user_repository(session: Session = Depends(get_session)) -> UserRepositoryProtocol:
    return UserRepository(session)

def get_candidate_repository(session: Session = Depends(get_session)) -> CandidateRepositoryProtocol:
    return CandidateRepository(session)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    id: int = int(payload.get("sub"))
    if id is None:
        raise InvalidTokenError
    return {"id": id}

