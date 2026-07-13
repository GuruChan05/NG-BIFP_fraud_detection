from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    merchant: str
    merchant_category: str
    location: str
    device_id: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    risk_score: float
    is_fraudulent: str
    created_at: datetime

    class Config:
        from_attributes = True
