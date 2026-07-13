from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.audit_log import AuditLog

class AuditLogger:
    @staticmethod
    def log_action(db: Session, user_id: int, action: str, resource_type: str, resource_id: int, details: dict = None):
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            timestamp=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
        return audit_log
