from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from src.config import settings
from src.commons.schemas import BaseApiResponse
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

async def invalid_token_exception_handler(request: Request, exc: InvalidTokenError):
    return BaseApiResponse(message="Invalid Token", status_code=status.HTTP_401_UNAUTHORIZED).make()

async def http_exception_handler(request: Request, exc: HTTPException):
    if settings.DEBUG == False and exc.status_code == 500:
        return BaseApiResponse(message="Internal Server Error", status_code=500).make()
        
    return BaseApiResponse(message=exc.detail, status_code=exc.status_code).make()

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return BaseApiResponse(message="Validation Error", errors=exc.errors(), status_code=422).make()

async def expired_token_exception_handler(request: Request, exc: ExpiredSignatureError):
    return BaseApiResponse(message="Expired Token", status_code=status.HTTP_401_UNAUTHORIZED).make()

async def generic_exception_handler(request: Request, exc: Exception):
    if settings.DEBUG == False and exc.status_code == 500 : 
        return BaseApiResponse(message="Internal Server Error", status_code=500).make()
        
    return BaseApiResponse(message=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR).make()

def register_exception_handler(app : FastAPI) : 
    app.add_exception_handler(InvalidTokenError, invalid_token_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ExpiredSignatureError, expired_token_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)