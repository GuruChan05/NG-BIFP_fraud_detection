from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TransactionSummary(BaseModel):
    id: int
    user_id: int
    amount: float
    transaction_type: str
    merchant: str
    risk_score: float
    is_fraudulent: str
    created_at: str


class DailySummary(BaseModel):
    date: str
    transactions: int
    fraud_count: int
    total_amount: float
    fraud_percentage: float


class FraudTrend(BaseModel):
    date: str
    fraud_count: int
    total_count: int
    fraud_rate: float


class RiskDistribution(BaseModel):
    very_low: int
    low: int
    medium: int
    high: int
    very_high: int
    total: int


class DashboardOverview(BaseModel):
    total_transactions: int
    fraud_cases: int
    active_users: int
    todays_activity: int
    average_risk_score: float
    trusted_devices: int
    high_risk_transactions: int
    resolved_alerts: int
    fraud_percentage: float


class TransactionStats(BaseModel):
    total_amount: float
    average_amount: float
    max_amount: float
    min_amount: float


class UserStats(BaseModel):
    total: int
    active: int
    admins: int


class SummaryStats(BaseModel):
    transactions: TransactionStats
    users: UserStats
    risk_distribution: RiskDistribution
