from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.notification import NotificationResponse, NotificationCreate

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.db.models.notification import Notification
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    return notifications

@router.post("/", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    from app.db.models.notification import Notification
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
