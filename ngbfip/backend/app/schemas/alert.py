from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AlertType(str, Enum):
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    HIGH_RISK = "high_risk"
    FRAUD_DETECTED = "fraud_detected"
    DEVICE_CHANGE = "device_change"
    UNUSUAL_PATTERN = "unusual_pattern"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertCreate(BaseModel):
    """Create alert request"""
    user_id: int
    transaction_id: Optional[int] = None
    alert_type: AlertType
    severity: AlertSeverity
    description: str

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    """Alert response model"""
    id: int
    user_id: int
    transaction_id: Optional[int]
    alert_type: str
    severity: str
    description: str
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True
