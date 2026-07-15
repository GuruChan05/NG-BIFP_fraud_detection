"""Alert service for alert management."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.alert import Alert
from app.core.audit import audit_logger
from app.core.logging import logger
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
import json


class AlertService:
    """Service for alert management operations."""
    
    @staticmethod
    def create_alert(
        db: Session,
        transaction_id: str,
        user_id: str,
        alert_type: str,
        severity: str,
        title: str,
        description: Optional[str] = None,
        risk_factors: Optional[List[str]] = None
    ) -> Alert:
        """Create a new alert.
        
        Args:
            db: Database session
            transaction_id: Transaction ID
            user_id: User ID
            alert_type: Type of alert
            severity: Severity level
            title: Alert title
            description: Alert description
            risk_factors: List of risk factors
            
        Returns:
            Created alert
        """
        try:
            alert = Alert(
                id=str(uuid.uuid4()),
                transaction_id=transaction_id,
                user_id=user_id,
                alert_type=alert_type,
                severity=severity,
                title=title,
                description=description,
                risk_factors=json.dumps(risk_factors or []),
                status="open",
                is_acknowledged=False
            )
            
            db.add(alert)
            db.commit()
            db.refresh(alert)
            
            logger.info(f"Alert created: {alert.id} for transaction {transaction_id}")
            audit_logger.log_action(
                user_id=user_id,
                action="CREATE_ALERT",
                resource_type="ALERT",
                resource_id=alert.id,
                details={"alert_type": alert_type, "severity": severity}
            )
            
            return alert
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating alert: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating alert"
            )
    
    @staticmethod
    def get_alert_by_id(db: Session, alert_id: str) -> Optional[Alert]:
        """Get alert by ID.
        
        Args:
            db: Database session
            alert_id: Alert ID
            
        Returns:
            Alert if found, None otherwise
        """
        return db.query(Alert).filter(Alert.id == alert_id).first()
    
    @staticmethod
    def get_open_alerts(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> List[Alert]:
        """Get all open alerts.
        
        Args:
            db: Database session
            skip: Number of results to skip
            limit: Maximum number of results
            
        Returns:
            List of open alerts
        """
        return db.query(Alert).filter(
            Alert.status == "open"
        ).order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_alerts_by_severity(
        db: Session,
        severity: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Alert]:
        """Get alerts by severity.
        
        Args:
            db: Database session
            severity: Severity level
            skip: Number of results to skip
            limit: Maximum number of results
            
        Returns:
            List of alerts
        """
        return db.query(Alert).filter(
            Alert.severity == severity
        ).order_by(desc(Alert.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def resolve_alert(
        db: Session,
        alert_id: str,
        status: str,
        resolved_by_user_id: str,
        resolution_notes: Optional[str] = None
    ) -> Optional[Alert]:
        """Resolve an alert.
        
        Args:
            db: Database session
            alert_id: Alert ID
            status: New status
            resolved_by_user_id: User ID resolving alert
            resolution_notes: Resolution notes
            
        Returns:
            Updated alert
        """
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        
        if not alert:
            return None
        
        try:
            alert.status = status
            alert.resolved_by_user_id = resolved_by_user_id
            alert.resolution_notes = resolution_notes
            alert.resolved_at = datetime.utcnow()
            
            db.commit()
            db.refresh(alert)
            
            audit_logger.log_action(
                user_id=resolved_by_user_id,
                action="RESOLVE_ALERT",
                resource_type="ALERT",
                resource_id=alert_id,
                details={"status": status, "notes": resolution_notes}
            )
            
            return alert
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error resolving alert: {str(e)}")
            raise


alert_service = AlertService()
