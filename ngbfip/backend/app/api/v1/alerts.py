from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.alert import AlertResponse, AlertCreate

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.db.models.alert import Alert
    alerts = db.query(Alert).offset(skip).limit(limit).all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    from app.db.models.alert import Alert
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    from app.db.models.alert import Alert
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
