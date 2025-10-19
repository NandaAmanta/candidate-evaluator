from fastapi import APIRouter

router = APIRouter()

@router.get("/candidates")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/upload")
async def upload_file(file: bytes = None):
    return {"file_size": len(file)}

@router.patch("/evaluate")
async def evaluate(file: bytes = None):
    return {"file_size": len(file)}