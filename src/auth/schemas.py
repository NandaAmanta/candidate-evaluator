from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from src.auth.models import User

class UserCreation(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    password: str = Field(..., min_length=6, max_length=72)

class Token (BaseModel):
    access_token: str
    refresh_token: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password : Optional[str]

class Login(BaseModel):
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=6)

class UserRead(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: Optional[int] = None

    @staticmethod
    def from_orm(orm_obj : User) : 
        return UserRead(
            id=orm_obj.id,
            name=orm_obj.name,
            email=orm_obj.email,
            age=orm_obj.age,
        )
    
    
class UserReadWithToken (UserRead):
    token : Token 

    @staticmethod
    def from_orm(orm_obj : User, access_token : str, refresh_token : str) : 
        return UserReadWithToken(
            id=orm_obj.id,
            name=orm_obj.name,
            email=orm_obj.email,
            age=orm_obj.age,
            token=Token(access_token=access_token, refresh_token=refresh_token)
        )
        