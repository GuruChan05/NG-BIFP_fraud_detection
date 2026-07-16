"""Fraud prediction schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level categories."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FraudPredictionRequest(BaseModel):
    """Request schema for fraud prediction."""
    user_id: int
    amount: float = Field(..., gt=0)
    transaction_type: str
    merchant: str
    merchant_category: Optional[str] = None
    location: Optional[str] = None
    device_id: Optional[str] = None
    

class FraudPredictionResponse(BaseModel):
    """Response schema for fraud prediction."""
    transaction_id: Optional[int] = None
    risk_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    is_fraudulent: str  # "legitimate", "fraudulent", "suspicious"
    risk_level: RiskLevel
    explanation: str
    contributing_factors: List[str]
    recommendations: List[str]
    prediction_timestamp: datetime


class PredictionHistoryEntry(BaseModel):
    """Schema for prediction history entry."""
    id: int
    user_id: int
    transaction_id: Optional[int]
    risk_score: float
    confidence_score: float
    is_fraudulent: str
    risk_level: str
    explanation: str
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionHistoryResponse(BaseModel):
    """Response schema for prediction history list."""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[PredictionHistoryEntry]


class BulkPredictionRequest(BaseModel):
    """Request schema for bulk predictions."""
    transactions: List[FraudPredictionRequest]


class BulkPredictionResponse(BaseModel):
    """Response schema for bulk predictions."""
    total: int
    successful: int
    failed: int
    predictions: List[FraudPredictionResponse]
