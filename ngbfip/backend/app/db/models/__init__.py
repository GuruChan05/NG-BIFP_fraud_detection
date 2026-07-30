"""Update models __init__.py to include new models."""
from app.db.models.user import User
from app.db.models.transaction import Transaction
from app.db.models.alert import Alert
from app.db.models.device import Device
from app.db.models.notification import Notification
from app.db.models.audit_log import AuditLog
from app.db.models.fraud_prediction import FraudPrediction
from app.db.models.login_history import LoginHistory
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.system_log import SystemLog

__all__ = [
    "User",
    "Transaction",
    "Alert",
    "Device",
    "Notification",
    "AuditLog",
    "FraudPrediction",
    "LoginHistory",
    "Role",
    "Permission",
    "SystemLog",
]
