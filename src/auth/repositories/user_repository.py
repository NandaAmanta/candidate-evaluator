from typing import Optional
from sqlalchemy.orm import Session
from src.auth.models import User
from src.auth.schemas import UserUpdate, UserCreation
from src.database import engine
from src.commons.base_repository import (
    BaseSQLAlchemyRepository,
    BaseRepositoryProtocol,
)
 

class UserRepositoryProtocol(BaseRepositoryProtocol[User, UserCreation, UserUpdate]):
    def find_by_email(self, email: str) -> Optional[User]:
        ...


class UserRepository(
    BaseSQLAlchemyRepository[User, UserCreation, UserUpdate],
    UserRepositoryProtocol,
):
    def __init__(self, session: Session = Session(engine)):
        super().__init__(User, session)

    def find_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
