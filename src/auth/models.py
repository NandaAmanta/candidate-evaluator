from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,List
from src.candidate.models import Candidate
from sqlalchemy.orm import Mapped, relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: Optional[int] = None 
    password : str