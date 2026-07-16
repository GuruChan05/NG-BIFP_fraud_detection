"""Dashboard service with business logic and aggregation queries."""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from app.db.models.transaction import Transaction
from app.db.models.user import User
from app.db.models.alert import Alert
from app.db.models.device import Device


class DashboardService:
    """Service for dashboard data aggregation and statistics."""

    @staticmethod
    def get_total_transactions(db: Session) -> int:
        """Get total count of transactions."""
        return db.query(func.count(Transaction.id)).scalar() or 0

    @staticmethod
    def get_fraud_cases(db: Session) -> int:
        """Get count of fraudulent transactions."""
        return db.query(func.count(Transaction.id)).filter(
            Transaction.is_fraudulent == "fraudulent"
        ).scalar() or 0

    @staticmethod
    def get_active_users(db: Session) -> int:
        """Get count of active users."""
        return db.query(func.count(User.id)).filter(
            User.is_active == True
        ).scalar() or 0

    @staticmethod
    def get_todays_activity(db: Session) -> int:
        """Get count of transactions created today."""
        today = datetime.utcnow().date()
        return db.query(func.count(Transaction.id)).filter(
            func.date(Transaction.created_at) == today
        ).scalar() or 0

    @staticmethod
    def get_average_risk_score(db: Session) -> float:
        """Get average risk score of all transactions."""
        result = db.query(func.avg(Transaction.risk_score)).scalar()
        return round(result or 0.0, 2)

    @staticmethod
    def get_trusted_devices(db: Session) -> int:
        """Get count of trusted devices."""
        return db.query(func.count(Device.id)).filter(
            Device.is_trusted == True
        ).scalar() or 0

    @staticmethod
    def get_high_risk_transactions(db: Session) -> int:
        """Get count of high-risk transactions (risk_score >= 0.7)."""
        return db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score >= 0.7
        ).scalar() or 0

    @staticmethod
    def get_resolved_alerts(db: Session) -> int:
        """Get count of resolved alerts."""
        return db.query(func.count(Alert.id)).filter(
            Alert.is_resolved == True
        ).scalar() or 0

    @staticmethod
    def get_risk_distribution(db: Session) -> List[Dict]:
        """Get distribution of transactions by risk level."""
        low_risk = db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score < 0.3
        ).scalar() or 0
        
        medium_risk = db.query(func.count(Transaction.id)).filter(
            and_(Transaction.risk_score >= 0.3, Transaction.risk_score < 0.6)
        ).scalar() or 0
        
        high_risk = db.query(func.count(Transaction.id)).filter(
            and_(Transaction.risk_score >= 0.6, Transaction.risk_score < 0.8)
        ).scalar() or 0
        
        critical_risk = db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score >= 0.8
        ).scalar() or 0

        total = low_risk + medium_risk + high_risk + critical_risk
        total = max(total, 1)  # Avoid division by zero

        return [
            {
                "risk_level": "low",
                "count": low_risk,
                "percentage": round((low_risk / total) * 100, 2),
            },
            {
                "risk_level": "medium",
                "count": medium_risk,
                "percentage": round((medium_risk / total) * 100, 2),
            },
            {
                "risk_level": "high",
                "count": high_risk,
                "percentage": round((high_risk / total) * 100, 2),
            },
            {
                "risk_level": "critical",
                "count": critical_risk,
                "percentage": round((critical_risk / total) * 100, 2),
            },
        ]

    @staticmethod
    def get_monthly_statistics(db: Session) -> List[Dict]:
        """Get transaction statistics grouped by month."""
        results = db.query(
            extract("year", Transaction.created_at).label("year"),
            extract("month", Transaction.created_at).label("month"),
            func.count(Transaction.id).label("transactions"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_cases"),
            func.avg(Transaction.risk_score).label("risk_score"),
        ).group_by(
            extract("year", Transaction.created_at),
            extract("month", Transaction.created_at),
        ).order_by(
            extract("year", Transaction.created_at),
            extract("month", Transaction.created_at),
        ).all()

        stats = []
        for year, month, transactions, fraud_cases, risk_score in results:
            stats.append({
                "month": f"{int(month):02d}/{int(year)}",
                "transactions": transactions or 0,
                "fraud_cases": fraud_cases or 0,
                "risk_score": round(risk_score or 0.0, 2),
            })
        return stats

    @staticmethod
    def get_weekly_statistics(db: Session) -> List[Dict]:
        """Get transaction statistics grouped by week."""
        results = db.query(
            extract("year", Transaction.created_at).label("year"),
            extract("week", Transaction.created_at).label("week"),
            func.count(Transaction.id).label("transactions"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_cases"),
            func.avg(Transaction.risk_score).label("risk_score"),
        ).group_by(
            extract("year", Transaction.created_at),
            extract("week", Transaction.created_at),
        ).order_by(
            extract("year", Transaction.created_at),
            extract("week", Transaction.created_at),
        ).all()

        stats = []
        for year, week, transactions, fraud_cases, risk_score in results:
            stats.append({
                "week": f"W{int(week):02d}/{int(year)}",
                "transactions": transactions or 0,
                "fraud_cases": fraud_cases or 0,
                "risk_score": round(risk_score or 0.0, 2),
            })
        return stats

    @staticmethod
    def get_recent_activity(db: Session, limit: int = 10) -> List[Dict]:
        """Get recent transactions."""
        transactions = db.query(Transaction).order_by(
            Transaction.created_at.desc()
        ).limit(limit).all()

        return [
            {
                "id": t.id,
                "user_id": t.user_id,
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "merchant": t.merchant,
                "risk_score": t.risk_score,
                "is_fraudulent": t.is_fraudulent,
                "created_at": t.created_at,
            }
            for t in transactions
        ]
