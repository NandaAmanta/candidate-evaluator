from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

M = TypeVar('M')

class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Number of items returned in the response')
    items: List[M] = Field(description='List of items returned in the response following given criteria')

class BaseApiResponse(BaseModel, Generic[M]):
    message: str
    status_code: int = 200
    data : Optional[M] = None
    errors : Optional[List] = None

    def make(self):
        response = {
            "message": self.message,
            "status_code": self.status_code,
            "data": jsonable_encoder(self.data),
        }
        if self.errors is not None:
            response["errors"] = self.errors
        
        return JSONResponse(content=response, status_code=self.status_code)