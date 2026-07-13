from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.notification import NotificationResponse, NotificationCreate

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implement list notifications
    pass

@router.post("/", response_model=NotificationResponse)
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    # TODO: Implement create notification
    pass
