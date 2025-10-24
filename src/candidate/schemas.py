from typing import Optional, List, Dict, Any
from sqlmodel import Field
from pydantic import BaseModel
from src.candidate.models import Candidate
from fastapi import UploadFile, File
import json

class CandidateCreation(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    cv_paths : str
    project_report_paths : str
    user_id: int

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    
class CandidateEvaluation(BaseModel):
    candidate_ids : List[int]

class CandidateRead(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    cv_paths : str
    project_report_paths : str
    user_id: Optional[int] = None
    status: Optional[str]
    evaluation_result_json : Optional[Dict[str, Any]] = None
    error : Optional[str]

    @staticmethod
    def from_orm(orm_obj : Candidate) : 
        # string to DICT
        if orm_obj.evaluation_result_json is not None:
            evaluation_result_json = json.loads(orm_obj.evaluation_result_json) 
        else:
            evaluation_result_json = None
        return CandidateRead(
            age=orm_obj.age,
            email=orm_obj.email,
            cv_paths=orm_obj.cv_paths,
            project_report_paths=orm_obj.project_report_paths,
            id=orm_obj.id,
            name=orm_obj.name,
            status=orm_obj.status,
            user_id=orm_obj.user_id,
            evaluation_result_json=evaluation_result_json,
            error=orm_obj.error
        )
    
class CvEvaluation(BaseModel):
    technical_skills: int
    experience_level: int
    achievements: int
    cultural_fit: int
    match_rate: float = 0.0
    feedback: str = ""

    def calculate_match_rate(self, weights: Dict[str, float]) -> float:
        total = (
            self.technical_skills * weights["technical_skills"]
            + self.experience_level * weights["experience_level"]
            + self.achievements * weights["achievements"]
            + self.cultural_fit * weights["cultural_fit"]
        )
        # max possible = 5 * sum(weights) -> normalize to 0..1
        max_score = 5 * sum(weights.values())
        self.match_rate = round(total / max_score, 2)
        return self.match_rate


class ProjectEvaluation(BaseModel):
    correctness: int
    code_quality: int
    resilience: int
    documentation: int
    creativity: int
    final_score: float = 0.0
    feedback: str = ""

    def calculate_final_score(self, weights: Dict[str, float]) -> float:
        total = (
            self.correctness * weights["correctness"]
            + self.code_quality * weights["code_quality"]
            + self.resilience * weights["resilience"]
            + self.documentation * weights["documentation"]
            + self.creativity * weights["creativity"]
        )
        max_score = 5 * sum(weights.values())
        # Convert to 1-5 scale for easier interpretation
        normalized = total / max_score * 5
        self.final_score = round(normalized, 2)
        return self.final_score
