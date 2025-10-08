from pydantic import BaseModel
from datetime import datetime

class BaseDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models

class BaseAuditDTO(BaseDTO):
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
