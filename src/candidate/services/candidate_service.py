
from fastapi import Depends, Request, UploadFile, BackgroundTasks
from typing import List
from src.candidate.repositories.candidate_repository import CandidateRepositoryProtocol
from src.dependencies import get_candidate_repository
from src.candidate.schemas import CandidateCreation, CandidateRead
from src.config import settings
import os
import uuid
from fastapi import HTTPException

class CandidateService:

    def __init__(self, repository : CandidateRepositoryProtocol = Depends(get_candidate_repository)) -> None:
        self.repository = repository

    def pagination(self, request: dict) :
        data = self.repository.paginate(request)
        data.items = [CandidateRead.from_orm(item) for item in data.items]
        return data

    async def create(self, cv_files: List[UploadFile], project_files: List[UploadFile], user_id: int):
        cv_paths : List[str] = []
        for file in cv_files:
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR, "cv", file_name)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            cv_paths.append(file_path)

        project_file_paths : List[str] = []
        for file in project_files:
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(settings.UPLOAD_DIR , "project", file_name)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            project_file_paths.append(file_path)
            
        return self.repository.create(
            CandidateCreation(
                cv_paths=",".join(map(str, cv_paths)),
                project_report_paths=",".join(map(str, project_file_paths)),
                user_id=user_id
            )
        )

    async def delete(self, id: int, user_id : int):
        data = self.repository.find_by_id(id)
        if(data.user_id != user_id):
            raise HTTPException(status_code=403, detail="Unauthorized")
        return self.repository.delete(id)
    