from __future__ import annotations
from sqlmodel import SQLModel, Field,Relationship
from typing import Optional

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    file_path : str 
    user_id: Optional[int] = Field(default=None, foreign_key="user.id") 
    status: Optional[str] = Field(default="QUEUED")
