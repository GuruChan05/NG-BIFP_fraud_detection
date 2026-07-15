from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class TransactionCreate(BaseModel):
    """Create transaction request"""
    amount: float = Field(..., gt=0)
    transaction_type: TransactionType
    merchant: str
    merchant_category: str
    location: str
    device_id: str

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    """Transaction response model"""
    id: int
    user_id: int
    amount: float
    transaction_type: str
    merchant: str
    merchant_category: str
    location: str
    device_id: str
    risk_score: float
    is_fraudulent: str
    created_at: datetime

    class Config:
        from_attributes = True
