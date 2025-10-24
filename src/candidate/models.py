from __future__ import annotations
from sqlmodel import SQLModel, Field,Relationship,Column
from sqlalchemy import JSON
from typing import Optional, Dict, Any

class Candidate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    cv_paths : str 
    project_report_paths : str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id") 
    status: Optional[str] = Field(default="QUEUED")
    evaluation_result_json : Optional[Dict[str, Any]] = Field(sa_column=Column(JSON))
    error : Optional[str]
