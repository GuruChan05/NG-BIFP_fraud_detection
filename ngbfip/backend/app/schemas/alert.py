"""Alert schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class AlertCreate(BaseModel):
    """Alert creation schema."""
    transaction_id: str
    user_id: str
    alert_type: str = Field(..., pattern="^(fraud|suspicious|warning)$")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    title: str
    description: Optional[str] = None
    risk_factors: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "alert_type": "fraud",
                "severity": "high",
                "title": "Potential Fraudulent Transaction",
                "description": "Transaction from unusual location",
                "risk_factors": ["Unusual location", "High amount"]
            }
        }


class AlertResponse(BaseModel):
    """Alert response schema."""
    id: str
    transaction_id: str
    alert_type: str
    severity: str
    title: str
    description: Optional[str]
    status: str
    is_acknowledged: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "transaction_id": "123e4567-e89b-12d3-a456-426614174001",
                "alert_type": "fraud",
                "severity": "high",
                "title": "Potential Fraudulent Transaction",
                "description": "Transaction from unusual location",
                "status": "open",
                "is_acknowledged": False,
                "created_at": "2024-01-01T12:00:00Z"
            }
        }


class AlertResolve(BaseModel):
    """Alert resolution schema."""
    status: str = Field(..., pattern="^(investigating|resolved|dismissed)$")
    resolution_notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "resolved",
                "resolution_notes": "Verified legitimate transaction"
            }
        }
