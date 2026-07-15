"""Device schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    """Device creation schema."""
    user_id: str
    device_name: str
    device_type: str = Field(..., pattern="^(mobile|desktop|tablet)$")
    os: Optional[str] = None
    device_fingerprint: str
    ip_address: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "device_name": "iPhone 14",
                "device_type": "mobile",
                "os": "iOS 17",
                "device_fingerprint": "abc123def456",
                "ip_address": "192.168.1.1"
            }
        }


class DeviceResponse(BaseModel):
    """Device response schema."""
    id: str
    user_id: str
    device_name: str
    device_type: str
    trust_score: float
    is_trusted: bool
    trust_level: Optional[str]
    created_at: datetime
    last_used: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "device_name": "iPhone 14",
                "device_type": "mobile",
                "trust_score": 0.85,
                "is_trusted": True,
                "trust_level": "high",
                "created_at": "2024-01-01T12:00:00Z",
                "last_used": "2024-01-15T10:30:00Z"
            }
        }


class DeviceTrustUpdate(BaseModel):
    """Device trust update schema."""
    is_trusted: bool
    trust_level: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_trusted": True,
                "trust_level": "high"
            }
        }
