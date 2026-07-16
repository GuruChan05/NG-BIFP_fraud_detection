"""Dashboard API endpoints with live PostgreSQL data."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.db.models.user import User
from app.services.dashboard import DashboardService
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardStatistics,
    RiskDistribution,
    MonthlyStatistic,
    WeeklyStatistic,
    RecentActivity,
    DashboardSummary,
)
from typing import List

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get dashboard overview with all key metrics.
    Returns: total transactions, fraud cases, active users, today's activity, etc.
    """
    try:
        return DashboardOverview(
            total_transactions=DashboardService.get_total_transactions(db),
            fraud_cases=DashboardService.get_fraud_cases(db),
            active_users=DashboardService.get_active_users(db),
            todays_activity=DashboardService.get_todays_activity(db),
            average_risk_score=DashboardService.get_average_risk_score(db),
            trusted_devices=DashboardService.get_trusted_devices(db),
            high_risk_transactions=DashboardService.get_high_risk_transactions(db),
            resolved_alerts=DashboardService.get_resolved_alerts(db),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard overview: {str(e)}",
        )


@router.get("/statistics", response_model=DashboardStatistics)
async def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get dashboard statistics.
    Returns: total transactions, fraud cases, average risk score, high-risk transactions.
    """
    try:
        return DashboardStatistics(
            total_transactions=DashboardService.get_total_transactions(db),
            fraud_cases=DashboardService.get_fraud_cases(db),
            average_risk_score=DashboardService.get_average_risk_score(db),
            high_risk_transactions=DashboardService.get_high_risk_transactions(db),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard statistics: {str(e)}",
        )


@router.get("/risk-distribution", response_model=List[RiskDistribution])
async def get_risk_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get risk distribution of transactions.
    Returns breakdown of transactions by risk level (low, medium, high, critical).
    """
    try:
        data = DashboardService.get_risk_distribution(db)
        return [
            RiskDistribution(
                risk_level=item["risk_level"],
                count=item["count"],
                percentage=item["percentage"],
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching risk distribution: {str(e)}",
        )


@router.get("/monthly-statistics", response_model=List[MonthlyStatistic])
async def get_monthly_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get monthly statistics.
    Returns transaction count, fraud cases, and average risk score per month.
    """
    try:
        data = DashboardService.get_monthly_statistics(db)
        return [
            MonthlyStatistic(
                month=item["month"],
                transactions=item["transactions"],
                fraud_cases=item["fraud_cases"],
                risk_score=item["risk_score"],
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching monthly statistics: {str(e)}",
        )


@router.get("/weekly-statistics", response_model=List[WeeklyStatistic])
async def get_weekly_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get weekly statistics.
    Returns transaction count, fraud cases, and average risk score per week.
    """
    try:
        data = DashboardService.get_weekly_statistics(db)
        return [
            WeeklyStatistic(
                week=item["week"],
                transactions=item["transactions"],
                fraud_cases=item["fraud_cases"],
                risk_score=item["risk_score"],
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching weekly statistics: {str(e)}",
        )


@router.get("/recent-activity", response_model=List[RecentActivity])
async def get_recent_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 10,
):
    """
    Get recent transactions/activity.
    Returns the most recent transactions up to the specified limit.
    """
    try:
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 10
        
        data = DashboardService.get_recent_activity(db, limit=limit)
        return [
            RecentActivity(
                id=item["id"],
                user_id=item["user_id"],
                amount=item["amount"],
                transaction_type=item["transaction_type"],
                merchant=item["merchant"],
                risk_score=item["risk_score"],
                is_fraudulent=item["is_fraudulent"],
                created_at=item["created_at"],
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching recent activity: {str(e)}",
        )


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get complete dashboard summary.
    Returns all dashboard data including overview, statistics, distributions, and recent activity.
    """
    try:
        overview = DashboardOverview(
            total_transactions=DashboardService.get_total_transactions(db),
            fraud_cases=DashboardService.get_fraud_cases(db),
            active_users=DashboardService.get_active_users(db),
            todays_activity=DashboardService.get_todays_activity(db),
            average_risk_score=DashboardService.get_average_risk_score(db),
            trusted_devices=DashboardService.get_trusted_devices(db),
            high_risk_transactions=DashboardService.get_high_risk_transactions(db),
            resolved_alerts=DashboardService.get_resolved_alerts(db),
        )
        
        risk_dist_data = DashboardService.get_risk_distribution(db)
        risk_distribution = [
            RiskDistribution(
                risk_level=item["risk_level"],
                count=item["count"],
                percentage=item["percentage"],
            )
            for item in risk_dist_data
        ]
        
        monthly_data = DashboardService.get_monthly_statistics(db)
        monthly_statistics = [
            MonthlyStatistic(
                month=item["month"],
                transactions=item["transactions"],
                fraud_cases=item["fraud_cases"],
                risk_score=item["risk_score"],
            )
            for item in monthly_data
        ]
        
        weekly_data = DashboardService.get_weekly_statistics(db)
        weekly_statistics = [
            WeeklyStatistic(
                week=item["week"],
                transactions=item["transactions"],
                fraud_cases=item["fraud_cases"],
                risk_score=item["risk_score"],
            )
            for item in weekly_data
        ]
        
        recent_act_data = DashboardService.get_recent_activity(db, limit=10)
        recent_activity = [
            RecentActivity(
                id=item["id"],
                user_id=item["user_id"],
                amount=item["amount"],
                transaction_type=item["transaction_type"],
                merchant=item["merchant"],
                risk_score=item["risk_score"],
                is_fraudulent=item["is_fraudulent"],
                created_at=item["created_at"],
            )
            for item in recent_act_data
        ]
        
        return DashboardSummary(
            overview=overview,
            risk_distribution=risk_distribution,
            monthly_statistics=monthly_statistics,
            weekly_statistics=weekly_statistics,
            recent_activity=recent_activity,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard summary: {str(e)}",
        )
