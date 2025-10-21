
from fastapi import Depends, Request, UploadFile
from src.candidate.repositories.candidate_repository import CandidateRepositoryProtocol
from src.dependencies import get_candidate_repository
from src.candidate.models import Candidate
from src.candidate.schemas import CandidateCreation
from src.config import settings
import os
import uuid

class CandidateService:

    def __init__(self, repository : CandidateRepositoryProtocol = Depends(get_candidate_repository)) -> None:
        self.repository = repository

    def pagination(self, request: dict):
        return self.repository.paginate(request)
    

    async def create(self, file: UploadFile, user_id: int):
        file_ext = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return self.repository.create(
            CandidateCreation(
                file_path=file_path,
                user_id=user_id
            )
        )