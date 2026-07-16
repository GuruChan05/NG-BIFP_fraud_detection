from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.core.middleware import LoggingMiddleware
from app.db.base import Base, engine
from app.db.models.user import User
from app.api.v1 import (
    auth,
    users,
    transactions,
    alerts,
    devices,
    notifications,
    dashboard,
    risk,
    health,
)

app = FastAPI(
    title="NG-BIFP Fraud Detection API",
    description="Next-Generation Bank Integrated Fraud Prevention",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["Risk"])

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
