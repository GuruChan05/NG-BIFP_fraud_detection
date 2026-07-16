from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db

router = APIRouter()

@router.get("/overview")
async def dashboard_overview(db: Session = Depends(get_db)):
    from app.db.models.transaction import Transaction
    from app.db.models.alert import Alert
    total_transactions = db.query(Transaction).count()
    active_alerts = db.query(Alert).filter(Alert.is_resolved == False).count()
    return {
        "total_transactions": total_transactions,
        "active_alerts": active_alerts
    }

@router.get("/statistics")
async def dashboard_statistics(db: Session = Depends(get_db)):
    return {
        "trend": [
            {"date": "2023-01-01", "count": 10},
            {"date": "2023-01-02", "count": 15},
            {"date": "2023-01-03", "count": 8}
        ]
    }
