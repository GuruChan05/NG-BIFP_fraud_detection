from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RiskMetric(BaseModel):
    """Risk metric model"""
    timestamp: datetime
    risk_level: str
    count: int

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_transactions: int
    total_alerts: int
    high_risk_transactions: int
    fraudulent_transactions: int
    average_risk_score: float
    devices_registered: int
    users_active: int

    class Config:
        from_attributes = True


class DashboardOverview(BaseModel):
    """Dashboard overview"""
    stats: DashboardStats
    recent_alerts: List[dict]
    risk_trends: List[RiskMetric]
    top_merchants: List[dict]

    class Config:
        from_attributes = True
