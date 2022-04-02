from typing import Optional

from .BaseModel import (MyBaseModel,BaseModel)

class BranchSchema(MyBaseModel):
    name: str
    description: str
    logo: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Branch Name",
                "description": "Branch Description",
                "logo": "Branch Logo",
            }
        }

class UpdateBranchSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Branch Name Updated",
                "description": "Branch Description Updated",
                "logo": "Branch Logo Updated",
            }
        }
        