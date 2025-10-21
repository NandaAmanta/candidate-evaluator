from typing import Optional
from sqlmodel import Field
from pydantic import BaseModel
from src.candidate.models import Candidate
from fastapi import UploadFile, File

class CandidateCreation(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    file_path : str
    user_id: int

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    
class CanidateRead(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: Optional[int] = None
    file_path : str
    user_id: Optional[int] = None

    @staticmethod
    def from_orm(orm_obj : Candidate) : 
        return CanidateRead(
            age=orm_obj.age,
            email=orm_obj.email,
            file_path=orm_obj.file_path,
            id=orm_obj.id,
            name=orm_obj.name,
        )