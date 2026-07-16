"""Dashboard Pydantic schemas for response validation."""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class DashboardOverview(BaseModel):
    """Dashboard overview statistics."""
    total_transactions: int
    fraud_cases: int
    active_users: int
    todays_activity: int
    average_risk_score: float
    trusted_devices: int
    high_risk_transactions: int
    resolved_alerts: int


class RiskDistribution(BaseModel):
    """Risk distribution data."""
    risk_level: str  # low, medium, high, critical
    count: int
    percentage: float


class MonthlyStatistic(BaseModel):
    """Monthly statistics data."""
    month: str
    transactions: int
    fraud_cases: int
    risk_score: float


class WeeklyStatistic(BaseModel):
    """Weekly statistics data."""
    week: str
    transactions: int
    fraud_cases: int
    risk_score: float


class RecentActivity(BaseModel):
    """Recent activity/transaction data."""
    id: int
    user_id: int
    amount: float
    transaction_type: str
    merchant: str
    risk_score: float
    is_fraudulent: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStatistics(BaseModel):
    """Dashboard statistics response."""
    total_transactions: int
    fraud_cases: int
    average_risk_score: float
    high_risk_transactions: int


class DashboardSummary(BaseModel):
    """Complete dashboard summary."""
    overview: DashboardOverview
    risk_distribution: List[RiskDistribution]
    monthly_statistics: List[MonthlyStatistic]
    weekly_statistics: List[WeeklyStatistic]
    recent_activity: List[RecentActivity]

    class Config:
        from_attributes = True
