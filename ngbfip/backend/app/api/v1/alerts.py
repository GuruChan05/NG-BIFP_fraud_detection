from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.alert import AlertResponse, AlertCreate

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implement list alerts
    pass

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    # TODO: Implement get alert
    pass

@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    # TODO: Implement create alert
    pass
