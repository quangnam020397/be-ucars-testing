from typing import Optional

from .BaseModel import (MyBaseModel,BaseModel)
from bson.objectid import ObjectId

class CarSchema(MyBaseModel):
    name: str
    branch_id: str
    description: str
    thumbnail: str = None
    images: list = []
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Car Name",
                "branch_id": "Branch ID",
                "description": "Car Description",
            }
        }

class UpdateCarSchema(BaseModel):
    name: Optional[str] = None
    branch_id: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Car Name Updated",
                "branch_id": "Branch ID Updated",
                "description": "Car Description Updated",
                "thumbnail": "Car thumbnail Updated",
            }
        }
        