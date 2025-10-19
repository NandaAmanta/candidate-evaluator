from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from src.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_ACCESS_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_REFRESH_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
    
def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_REFRESH_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except InvalidTokenError:
        return None