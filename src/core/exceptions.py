from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from src.config import settings
from src.core.api_response import BaseApiResponse

# Custom handler untuk HTTPException
async def http_exception_handler(request: Request, exc: HTTPException):
    if settings.DEBUG == False and exc.status_code == 500:
        return BaseApiResponse(message="Internal Server Error", status_code=500).make()
        
    return BaseApiResponse(message=exc.detail, status_code=exc.status_code).make()

# Handler untuk validation error (Pydantic)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return BaseApiResponse(message="Validation Error", error=exc.errors(), status_code=422).make()

# Handler untuk semua exception lain (server error)
async def generic_exception_handler(request: Request, exc: Exception):
    if settings.DEBUG == False and exc.status_code == 500 : 
        return BaseApiResponse(message="Internal Server Error", status_code=500).make()
        
    return BaseApiResponse(message=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).make()

def register_exception_handler(app : FastAPI) : 
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)