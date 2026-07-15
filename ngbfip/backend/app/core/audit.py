"""Audit logging for compliance and tracking."""
from datetime import datetime
from typing import Optional, Any, Dict
from app.core.logging import logger
from app.core.config import settings


class AuditLogger:
    """Centralized audit logging system."""
    
    @staticmethod
    def log_action(
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: Optional[str],
        details: Optional[Dict[str, Any]] = None,
        status: str = "SUCCESS"
    ) -> None:
        """Log an action for audit trail.
        
        Args:
            user_id: ID of user performing action
            action: Type of action (CREATE, READ, UPDATE, DELETE, LOGIN, etc.)
            resource_type: Type of resource being acted upon
            resource_id: ID of resource
            details: Additional details about the action
            status: Status of action (SUCCESS, FAILURE)
        """
        if not settings.ENABLE_AUDIT_LOGGING:
            return
        
        timestamp = datetime.utcnow().isoformat()
        audit_entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "status": status,
            "details": details or {}
        }
        
        logger.info(f"AUDIT: {audit_entry}")
    
    @staticmethod
    def log_login(user_id: str, success: bool, ip_address: Optional[str] = None) -> None:
        """Log login attempt.
        
        Args:
            user_id: User ID attempting login
            success: Whether login was successful
            ip_address: IP address of login attempt
        """
        AuditLogger.log_action(
            user_id=user_id,
            action="LOGIN",
            resource_type="USER",
            resource_id=user_id,
            details={"ip_address": ip_address, "success": success},
            status="SUCCESS" if success else "FAILURE"
        )
    
    @staticmethod
    def log_api_call(
        user_id: Optional[str],
        endpoint: str,
        method: str,
        status_code: int
    ) -> None:
        """Log API call.
        
        Args:
            user_id: ID of user making call
            endpoint: API endpoint called
            method: HTTP method
            status_code: Response status code
        """
        AuditLogger.log_action(
            user_id=user_id,
            action=f"API_CALL_{method}",
            resource_type="API",
            resource_id=endpoint,
            details={"endpoint": endpoint, "method": method, "status_code": status_code},
            status="SUCCESS" if status_code < 400 else "FAILURE"
        )
    
    @staticmethod
    def log_transaction_analysis(
        user_id: str,
        transaction_id: str,
        risk_score: float,
        risk_level: str
    ) -> None:
        """Log transaction risk analysis.
        
        Args:
            user_id: User ID analyzing transaction
            transaction_id: Transaction ID analyzed
            risk_score: Computed risk score
            risk_level: Risk level classification
        """
        AuditLogger.log_action(
            user_id=user_id,
            action="ANALYZE_RISK",
            resource_type="TRANSACTION",
            resource_id=transaction_id,
            details={
                "risk_score": risk_score,
                "risk_level": risk_level
            }
        )


audit_logger = AuditLogger()
