from fastapi import APIRouter, Depends
from src.dependencies import get_current_user
from src.candidate.services.candidate_service import CandidateService
from src.commons.schemas import BaseApiResponse
from src.auth.models import Candidate

router = APIRouter(prefix="/candidates", tags=["candidate"])

@router.get('')
async def pagination( 
    user = Depends(get_current_user), 
    service: CandidateService = Depends()) -> BaseApiResponse: 
    candidates = []
    return BaseApiResponse(data=candidates, message="Success", status_code=200).make()