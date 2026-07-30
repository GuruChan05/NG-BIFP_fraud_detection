from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.dashboard import DashboardService
from app.schemas.dashboard import DashboardOverview, SummaryStats
from app.db.models.user import User
from app.api.deps import get_current_active_user
from typing import List

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard overview statistics."""
    return DashboardService.get_overview(db)


@router.get("/summary", response_model=SummaryStats)
async def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get comprehensive summary statistics."""
    return DashboardService.get_summary_stats(db)


@router.get("/recent-transactions")
async def get_recent_transactions(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get recent transactions."""
    return DashboardService.get_recent_transactions(db, limit)


@router.get("/daily-summary")
async def get_daily_summary(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get daily transaction summary."""
    return DashboardService.get_daily_summary(db, days)


@router.get("/fraud-trends")
async def get_fraud_trends(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get fraud trends."""
    return DashboardService.get_fraud_trends(db, days)


@router.get("/risk-distribution")
async def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get risk score distribution."""
    return DashboardService.get_risk_distribution(db)
