from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DeviceType(str, Enum):
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"
    UNKNOWN = "unknown"


class TrustStatus(str, Enum):
    UNKNOWN = "unknown"
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"


class DeviceCreate(BaseModel):
    """Create device request"""
    device_id: str
    device_type: DeviceType
    os: str
    browser: str

    class Config:
        from_attributes = True


class DeviceResponse(BaseModel):
    """Device response model"""
    id: int
    device_id: str
    user_id: int
    device_type: str
    os: str
    browser: str
    trust_score: float
    is_trusted: str
    last_seen: datetime
    created_at: datetime

    class Config:
        from_attributes = True
