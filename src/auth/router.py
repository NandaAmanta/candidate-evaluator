from fastapi import APIRouter, Depends
from src.auth.schemas import UserRead, UserCreation, Login,UserReadWithToken
from src.auth.services.auth_service import AuthService
from src.commons.schemas import BaseApiResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login_for_access_token(data : Login, service: AuthService = Depends()):
    user = service.login(data)
    return BaseApiResponse[UserReadWithToken](data=user, message="Success", status_code=200)


@router.post("/registration", status_code=201)
async def register_new_user(data : UserCreation, service: AuthService = Depends()):
    user = service.register(data) 
    return BaseApiResponse[UserRead](data=user, message="User registered successfully", status_code=201)
