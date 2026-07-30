"""Transaction Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Transaction types."""
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER = "transfer"


class FraudStatus(str, Enum):
    """Fraud detection status."""
    UNKNOWN = "unknown"
    LEGITIMATE = "legitimate"
    FRAUDULENT = "fraudulent"


class TransactionCreate(BaseModel):
    """Schema for creating a transaction."""
    user_id: int
    amount: float = Field(..., gt=0)
    transaction_type: TransactionType
    merchant: str
    merchant_category: Optional[str] = None
    location: Optional[str] = None
    device_id: Optional[str] = None
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    is_fraudulent: FraudStatus = FraudStatus.UNKNOWN


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[TransactionType] = None
    merchant: Optional[str] = None
    merchant_category: Optional[str] = None
    location: Optional[str] = None
    device_id: Optional[str] = None
    risk_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_fraudulent: Optional[FraudStatus] = None


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    user_id: int
    amount: float
    transaction_type: str
    merchant: str
    merchant_category: Optional[str]
    location: Optional[str]
    device_id: Optional[str]
    risk_score: float
    is_fraudulent: str
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    """Schema for transaction list with pagination."""
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[TransactionResponse]


class TransactionStats(BaseModel):
    """Schema for transaction statistics."""
    total_transactions: int
    total_amount: float
    average_amount: float
    fraud_count: int
    fraud_percentage: float
    legitimate_count: int
    unknown_count: int


class BulkImportResponse(BaseModel):
    """Schema for bulk import response."""
    total_imported: int
    successful: int
    failed: int
    errors: List[str] = []

    class Config:
        from_attributes = True
