from fastapi import APIRouter, Depends
import random
from sqlalchemy.orm import Session
from app.db.base import get_db

router = APIRouter()

@router.post("/analyze")
async def analyze_risk(transaction_data: dict, db: Session = Depends(get_db)):
    return {"risk_score": round(random.uniform(0, 1), 2)}

@router.get("/trends")
async def risk_trends(db: Session = Depends(get_db)):
    return {"trends": [{"date": "2023-01-01", "risk": 0.2}, {"date": "2023-01-02", "risk": 0.5}]}
