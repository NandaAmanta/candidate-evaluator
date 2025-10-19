from app.routers import users, candidates
from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)
app.include_router(candidates.router)

