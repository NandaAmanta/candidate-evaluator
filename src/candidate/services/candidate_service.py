
from fastapi import Depends, Request
from src.candidate.repositories.candidate_repository import CandidateRepositoryProtocol
from src.dependencies import get_candidate_repository
from src.auth.models import Candidate

class CandidateService:

    def __init__(self, repository : CandidateRepositoryProtocol = Depends(get_candidate_repository)) -> None:
        self.repository = repository

    def pagination(self, request: dict):
        return self.repository.paginate(request)