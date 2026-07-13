from sqlalchemy.orm import Session
from app.db.models.notification import Notification
from datetime import datetime

class NotificationService:
    @staticmethod
    def get_notification_by_id(db: Session, notification_id: int):
        return db.query(Notification).filter(Notification.id == notification_id).first()

    @staticmethod
    def list_notifications(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        query = db.query(Notification)
        if user_id:
            query = query.filter(Notification.user_id == user_id)
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_notification(db: Session, notification_data: dict):
        notification = Notification(**notification_data)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
