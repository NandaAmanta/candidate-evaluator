
from fastapi import Depends, HTTPException
from src.auth.repositories.user_repository import UserRepositoryProtocol
from src.dependencies import get_user_repository
from src.auth.schemas import UserCreation, UserRead, Login, Token, UserReadWithToken
from src.auth.utils.hash import hash_password, verify_password
from src.auth.utils.jwt import create_access_token, create_refresh_token

class AuthService:
    def __init__(self, repository : UserRepositoryProtocol = Depends(get_user_repository)) -> None:
        self.repository = repository

    def login(self, data : Login) -> UserReadWithToken:
        user = self.repository.find_by_email(data.email)
        if (user is None ) or (not verify_password(data.password, user.password)):
            raise HTTPException(status_code=403 ,detail="Invalid credentials")
        
        access_token = create_access_token({"sub" : str(user.id)})
        refresh_token = create_refresh_token({"sub" : str(user.id)})
        return UserReadWithToken.from_orm(user, access_token, refresh_token)
    
    def register(self, data : UserCreation) -> UserRead:
        if self.repository.find_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        data.password = hash_password(data.password)
        return UserRead.from_orm(self.repository.create(data))