from fastapi import APIRouter, Depends
from src.auth.schemas import UserRead, UserCreation, Login
from src.auth.services.auth_service import AuthService
from src.core.api_response import BaseApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login_for_access_token(data : Login, service: AuthService = Depends()):
    user = service.login(data)
    return BaseApiResponse(data=user.dict(), message="User logged in successfully", status_code=200)

@router.post("/registration", status_code=201)
async def register_new_user(data : UserCreation, service: AuthService = Depends()):
    user = service.register(data) 
    return BaseApiResponse(data=user.dict(), message="User registered successfully", status_code=201)
