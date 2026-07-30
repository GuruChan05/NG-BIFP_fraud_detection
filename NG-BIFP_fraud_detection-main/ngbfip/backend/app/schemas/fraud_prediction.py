from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FraudPredictionBase(BaseModel):
    transaction_id: int
    risk_score: float
    confidence_score: float
    prediction: str
    explanation: Optional[str] = None


class FraudPredictionCreate(FraudPredictionBase):
    pass


class FraudPredictionResponse(FraudPredictionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
