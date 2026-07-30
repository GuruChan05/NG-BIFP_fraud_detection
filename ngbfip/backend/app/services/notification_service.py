"""Notification service with business logic and data operations."""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.db.models.notification import Notification
from app.db.models.user import User
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class NotificationService:
    """Service for notification management and operations."""

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info",
        related_transaction_id: Optional[int] = None,
        related_alert_id: Optional[int] = None,
    ) -> Notification:
        """Create a new notification for a user."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            related_transaction_id=related_transaction_id,
            related_alert_id=related_alert_id,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_notification_by_id(db: Session, notification_id: int) -> Optional[Notification]:
        """Get a notification by ID."""
        return db.query(Notification).filter(Notification.id == notification_id).first()

    @staticmethod
    def list_notifications(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        unread_only: bool = False,
    ) -> tuple[List[Notification], int]:
        """List notifications for a user with pagination."""
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        total = query.count()
        notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return notifications, total

    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return db.query(func.count(Notification.id)).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).scalar() or 0

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> Optional[Notification]:
        """Mark a notification as read."""
        notification = db.query(Notification).filter(
            and_(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
        ).first()
        
        if notification:
            notification.is_read = True
            notification.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(notification)
        
        return notification

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        count = db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).update({"is_read": True, "updated_at": datetime.utcnow()})
        db.commit()
        return count

    @staticmethod
    def bulk_mark_as_read(db: Session, notification_ids: List[int], user_id: int) -> int:
        """Mark multiple notifications as read."""
        count = db.query(Notification).filter(
            and_(
                Notification.id.in_(notification_ids),
                Notification.user_id == user_id
            )
        ).update({"is_read": True, "updated_at": datetime.utcnow()})
        db.commit()
        return count

    @staticmethod
    def delete_notification(db: Session, notification_id: int, user_id: int) -> bool:
        """Delete a notification."""
        notification = db.query(Notification).filter(
            and_(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
        ).first()
        
        if notification:
            db.delete(notification)
            db.commit()
            return True
        
        return False

    @staticmethod
    def delete_multiple(db: Session, notification_ids: List[int], user_id: int) -> int:
        """Delete multiple notifications."""
        count = db.query(Notification).filter(
            and_(
                Notification.id.in_(notification_ids),
                Notification.user_id == user_id
            )
        ).delete()
        db.commit()
        return count

    @staticmethod
    def clear_old_notifications(db: Session, user_id: int, days: int = 30) -> int:
        """Clear notifications older than specified days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        count = db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.created_at < cutoff_date
            )
        ).delete()
        db.commit()
        return count

    @staticmethod
    def get_notification_history(
        db: Session,
        user_id: int,
        days: int = 30,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[Notification], int]:
        """Get notification history for a user."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.created_at >= cutoff_date
            )
        )
        
        total = query.count()
        notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return notifications, total

    @staticmethod
    def get_notifications_by_type(
        db: Session,
        user_id: int,
        notification_type: str,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Notification], int]:
        """Get notifications filtered by type."""
        query = db.query(Notification).filter(
            and_(
                Notification.user_id == user_id,
                Notification.notification_type == notification_type
            )
        )
        
        total = query.count()
        notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return notifications, total

    @staticmethod
    def get_notification_stats(db: Session, user_id: int) -> Dict:
        """Get notification statistics for a user."""
        total = db.query(func.count(Notification.id)).filter(
            Notification.user_id == user_id
        ).scalar() or 0
        
        unread = db.query(func.count(Notification.id)).filter(
            and_(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).scalar() or 0
        
        read = total - unread
        
        # Get breakdown by type
        by_type_results = db.query(
            Notification.notification_type,
            func.count(Notification.id).label("count")
        ).filter(
            Notification.user_id == user_id
        ).group_by(Notification.notification_type).all()
        
        by_type = {item[0]: item[1] for item in by_type_results}
        
        return {
            "total_notifications": total,
            "unread_count": unread,
            "read_count": read,
            "by_type": by_type,
        }

    @staticmethod
    def create_fraud_notification(
        db: Session,
        user_id: int,
        transaction_id: int,
        fraud_risk_score: float,
    ) -> Notification:
        """Create a fraud alert notification."""
        risk_level = "Critical" if fraud_risk_score >= 0.8 else "High" if fraud_risk_score >= 0.6 else "Medium"
        
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=f"{risk_level} Risk Fraud Alert",
            message=f"Transaction #{transaction_id} flagged with {risk_level} fraud risk (Score: {fraud_risk_score:.2%})",
            notification_type="alert",
            related_transaction_id=transaction_id,
        )

    @staticmethod
    def create_alert_notification(
        db: Session,
        user_id: int,
        alert_id: int,
        alert_title: str,
    ) -> Notification:
        """Create an alert notification linked to an alert."""
        return NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=f"Alert: {alert_title}",
            message=f"A new alert has been generated: {alert_title}",
            notification_type="alert",
            related_alert_id=alert_id,
        )
