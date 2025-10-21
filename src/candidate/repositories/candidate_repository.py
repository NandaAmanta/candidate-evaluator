from typing import Optional
from sqlalchemy.orm import Session
from src.candidate.models import Candidate
from src.candidate.schemas import CandidateCreation,CandidateUpdate
from src.database import engine
from src.commons.base_repository import (
    BaseSQLAlchemyRepository,
    BaseRepositoryProtocol,
)
 
class CandidateRepositoryProtocol(BaseRepositoryProtocol[Candidate, CandidateCreation, CandidateUpdate]):
        ...


class CandidateRepository(
    BaseSQLAlchemyRepository[Candidate, CandidateCreation, CandidateUpdate],
    CandidateRepositoryProtocol,
):
    def __init__(self, session: Session = Session(engine)):
        super().__init__(Candidate, session)
