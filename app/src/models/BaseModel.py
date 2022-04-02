from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MyBaseModel(BaseModel):
    created_at: str = datetime.now()
    updated_at: str = datetime.now()
    deleted_at: Optional[str] = None
    
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}