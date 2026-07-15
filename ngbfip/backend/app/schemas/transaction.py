"""Transaction schemas for request/response validation."""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    """Transaction creation schema."""
    user_id: str
    device_id: Optional[str] = None
    amount: Decimal = Field(..., gt=0)
    currency: str = "USD"
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None
    transaction_type: str = Field(..., pattern="^(debit|credit|transfer)$")
    description: Optional[str] = None
    transaction_date: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "amount": 150.50,
                "currency": "USD",
                "merchant_name": "Amazon",
                "merchant_category": "Retail",
                "transaction_type": "debit",
                "transaction_date": "2024-01-01T12:00:00Z"
            }
        }


class TransactionResponse(BaseModel):
    """Transaction response schema."""
    id: str
    user_id: str
    amount: Decimal
    currency: str
    merchant_name: Optional[str]
    transaction_type: str
    risk_score: float
    risk_level: Optional[str]
    is_flagged: bool
    status: str
    created_at: datetime
    transaction_date: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "amount": 150.50,
                "currency": "USD",
                "merchant_name": "Amazon",
                "transaction_type": "debit",
                "risk_score": 0.25,
                "risk_level": "low",
                "is_flagged": False,
                "status": "approved",
                "created_at": "2024-01-01T12:00:00Z",
                "transaction_date": "2024-01-01T12:00:00Z"
            }
        }


class RiskAnalysisRequest(BaseModel):
    """Risk analysis request schema."""
    transaction_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class RiskAnalysisResponse(BaseModel):
    """Risk analysis response schema."""
    transaction_id: str
    risk_score: float
    risk_level: str
    anomaly_score: Optional[float] = None
    device_trust_score: Optional[float] = None
    risk_factors: list[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
                "risk_score": 0.35,
                "risk_level": "medium",
                "anomaly_score": 0.4,
                "device_trust_score": 0.8,
                "risk_factors": ["Unusual merchant", "New device"]
            }
        }
