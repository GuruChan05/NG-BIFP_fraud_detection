from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    device_id: str
    device_type: str
    os: str
    browser: str

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    id: int
    user_id: int
    trust_score: float
    is_trusted: str
    last_seen: datetime
    created_at: datetime

    class Config:
        from_attributes = True
