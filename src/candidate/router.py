from fastapi import APIRouter, Depends, Request, UploadFile, File, BackgroundTasks
from src.dependencies import get_current_user
from src.candidate.services.candidate_service import CandidateService 
from src.candidate.services.evaluation_service import EvaluationService
from src.commons.schemas import BaseApiResponse
from src.candidate.schemas import CandidateEvaluation
from typing import List

router = APIRouter(prefix="/candidates", tags=["candidate"])

@router.get('')
async def pagination(request: Request, user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse: 
    queries = dict(request.query_params)
    queries["user_id"] = user["id"]
    data = service.pagination(queries)
    return BaseApiResponse(data=data, message="Success", status_code=200).make()

@router.get('/{id}', status_code=200)
async def detail(id: int, user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse:
    data = service.detail(id, user["id"])
    return BaseApiResponse(data=data, message="Success", status_code=200).make()

@router.post('/upload', status_code=201)
async def create_candidate(cv_files: List[UploadFile] = File(..., description="List of cv files to upload"), project_files: List[UploadFile] = File(..., description="List of project files to upload"), user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse:
    data = await service.create(cv_files, project_files, user["id"])
    return BaseApiResponse(data=data, message="Success", status_code=201).make()

@router.delete('/{id}', status_code=200)
async def delete_candidate(id: int, user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse:
    return BaseApiResponse(data=service.delete(id, user["id"]), message="Success", status_code=200).make()


@router.post('/evaluate', status_code=200)
async def evaluate_candidate( background_tasks: BackgroundTasks, data : CandidateEvaluation, user = Depends(get_current_user), service: EvaluationService  = Depends()) -> BaseApiResponse:
    service.evaluate(data.candidate_ids, background_tasks)
    return BaseApiResponse(data={'data_processed_count' : len(data.candidate_ids)}, message="Success", status_code=200).make()

