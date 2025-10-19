# Import semua model dari tiap module biar Alembic bisa tahu metadata-nya
from src.auth.models import User
from src.candidate.models import Candidate

__all__ = ["User", "Candidate"]
