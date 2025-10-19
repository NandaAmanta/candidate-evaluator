from typing import Optional
from fastapi.responses import JSONResponse

class BaseApiResponse:
    def __init__(self, data: Optional[dict] = None, message: str = "", status_code: int = 200, error: Optional[dict] = None):
        self.data = data
        self.message = message
        self.status_code = status_code
        self.error = error

    def make(self):
        response = {
            "message": self.message,
            "status_code": self.status_code,
            "data": self.data
        }
        if self.error is not None:
            response["error"] = self.error
        
        return JSONResponse(content=response, status_code=self.status_code)
