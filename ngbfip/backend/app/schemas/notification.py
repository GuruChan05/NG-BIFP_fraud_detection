from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    ALERT = "alert"
    TRANSACTION = "transaction"
    DEVICE = "device"
    SYSTEM = "system"


class NotificationCreate(BaseModel):
    """Create notification request"""
    user_id: int
    title: str
    message: str
    notification_type: NotificationType
    related_id: Optional[int] = None

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    """Notification response model"""
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    related_id: Optional[int]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
