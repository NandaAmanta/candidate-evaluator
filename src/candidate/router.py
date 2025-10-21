from fastapi import APIRouter, Depends, Request, UploadFile, File
from src.dependencies import get_current_user
from src.candidate.services.candidate_service import CandidateService
from src.commons.schemas import BaseApiResponse
from src.candidate.models import Candidate

router = APIRouter(prefix="/candidates", tags=["candidate"])

@router.get('')
async def pagination(request: Request,user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse: 
    queries = dict(request.query_params)
    queries["user_id"] = user["id"]
    data = service.pagination(queries)
    return BaseApiResponse(data=data, message="Success", status_code=200).make()

@router.post('/upload', status_code=201)
async def create_candidate(file : UploadFile = File(...) , user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse:
    data = await service.create(file, user["id"])
    return BaseApiResponse(data=data, message="Success", status_code=201).make()

@router.post('/evaluate', status_code=201)
async def evaluate_candidate(user = Depends(get_current_user), service: CandidateService = Depends()) -> BaseApiResponse:
    return BaseApiResponse()

