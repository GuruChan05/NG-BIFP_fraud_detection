from fastapi import APIRouter
from app.api.v1 import auth, users, dashboard, transactions, fraud_predictions, admin
from app.api.v1 import notifications, devices, health, risk

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(fraud_predictions.router, prefix="/fraud-predictions", tags=["fraud-predictions"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(health.router, prefix="/health-check", tags=["health"])
api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
