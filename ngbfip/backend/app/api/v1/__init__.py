"""API v1 routes initialization."""
from . import auth, users, transactions, dashboard, fraud_predictions, alerts, devices, notifications, health

__all__ = [
    "auth",
    "users",
    "transactions",
    "dashboard",
    "fraud_predictions",
    "alerts",
    "devices",
    "notifications",
    "health",
]
