from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    alert_type: str
    severity: str
    description: str

class AlertCreate(AlertBase):
    user_id: int
    transaction_id: Optional[int] = None

class AlertResponse(AlertBase):
    id: int
    user_id: int
    transaction_id: Optional[int]
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True
