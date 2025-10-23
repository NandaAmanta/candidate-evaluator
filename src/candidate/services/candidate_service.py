
from fastapi import Depends, Request, UploadFile, BackgroundTasks
from typing import List
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

    async def create(self, files: List[UploadFile], user_id: int):
        file_paths : List[str] = []
        for file in files:
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, file_name)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            file_paths.append(file_path)
            
        return self.repository.create(
            CandidateCreation(
                file_path=", ".join(map(str, file_paths)),
                user_id=user_id
            )
        )

    async def evaluate(self, candidate_ids: List[int], background_tasks: BackgroundTasks) -> List[Candidate]:
        for candidate_id in candidate_ids:
            background_tasks.add_task(self.process_evaluation, candidate_id)            

    def process_evaluation(self, candidate_id : int) :
        candidate = self.repository.find_by_id(candidate_id)
        if(not candidate):
            return
            
        self.repository.update(candidate_id, {"status": "PROCESSING"})

        # TODO
        # Do evaluation

        
        self.repository.update(candidate_id, {"status": "COMPLATE"})

    