from sqlalchemy.orm import Session
from app.db.models.alert import Alert

class AlertService:
    @staticmethod
    def get_alert_by_id(db: Session, alert_id: int):
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def list_alerts(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        query = db.query(Alert)
        if user_id:
            query = query.filter(Alert.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_alert(db: Session, alert_data: dict):
        alert = Alert(**alert_data)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
