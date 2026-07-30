"""Notification Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    """Base notification schema."""
    title: str
    message: str
    notification_type: str = "info"


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    user_id: int
    related_transaction_id: Optional[int] = None
    related_alert_id: Optional[int] = None


class NotificationUpdate(BaseModel):
    """Schema for updating a notification."""
    is_read: Optional[bool] = None
    title: Optional[str] = None
    message: Optional[str] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    id: int
    user_id: int
    is_read: bool
    related_transaction_id: Optional[int] = None
    related_alert_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for notification list response."""
    total: int
    unread_count: int
    data: list[NotificationResponse]


class BulkMarkAsReadRequest(BaseModel):
    """Schema for bulk marking notifications as read."""
    notification_ids: list[int]


class NotificationStatsResponse(BaseModel):
    """Schema for notification statistics."""
    total_notifications: int
    unread_count: int
    read_count: int
    by_type: dict[str, int]
