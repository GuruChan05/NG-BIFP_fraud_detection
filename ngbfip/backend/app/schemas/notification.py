"""Notification schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NotificationCreate(BaseModel):
    """Notification creation schema."""
    user_id: str
    notification_type: str = Field(..., pattern="^(alert|warning|info)$")
    title: str
    message: str
    alert_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "notification_type": "alert",
                "title": "Suspicious Transaction Detected",
                "message": "A suspicious transaction has been detected on your account"
            }
        }


class NotificationResponse(BaseModel):
    """Notification response schema."""
    id: str
    user_id: str
    notification_type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "notification_type": "alert",
                "title": "Suspicious Transaction Detected",
                "message": "A suspicious transaction has been detected on your account",
                "is_read": False,
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
