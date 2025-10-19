
from sqlmodel import SQLModel, Field
from typing import Optional

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    file_path : str 
