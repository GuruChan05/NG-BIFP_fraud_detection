"""Enhanced Analytics service with comprehensive data aggregation."""
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from app.db.models.transaction import Transaction
from app.db.models.user import User
from app.db.models.alert import Alert
from app.db.models.device import Device
from app.db.models.fraud_prediction import FraudPrediction


class AnalyticsService:
    """Service for comprehensive analytics and reporting."""

    @staticmethod
    def get_hourly_fraud_trend(db: Session, days: int = 30) -> List[Dict]:
        """Get fraud trend by hour for the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        results = db.query(
            extract("day", Transaction.created_at).label("day"),
            extract("hour", Transaction.created_at).label("hour"),
            func.count(Transaction.id).label("total"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
        ).filter(
            Transaction.created_at >= cutoff_date
        ).group_by(
            extract("day", Transaction.created_at),
            extract("hour", Transaction.created_at),
        ).order_by(
            extract("day", Transaction.created_at),
            extract("hour", Transaction.created_at),
        ).all()

        trend = []
        for day, hour, total, fraud_count in results:
            trend.append({
                "day": int(day),
                "hour": int(hour),
                "total_transactions": total or 0,
                "fraud_count": fraud_count or 0,
                "fraud_percentage": (fraud_count / total * 100) if total > 0 else 0,
            })
        return trend

    @staticmethod
    def get_daily_fraud_trend(db: Session, days: int = 90) -> List[Dict]:
        """Get fraud trend by day for the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        results = db.query(
            func.date(Transaction.created_at).label("date"),
            func.count(Transaction.id).label("total"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
            func.avg(Transaction.risk_score).label("avg_risk"),
        ).filter(
            Transaction.created_at >= cutoff_date
        ).group_by(
            func.date(Transaction.created_at),
        ).order_by(
            func.date(Transaction.created_at),
        ).all()

        trend = []
        for date, total, fraud_count, avg_risk in results:
            trend.append({
                "date": str(date),
                "total_transactions": total or 0,
                "fraud_count": fraud_count or 0,
                "fraud_rate": (fraud_count / total * 100) if total > 0 else 0,
                "average_risk_score": round(avg_risk or 0.0, 3),
            })
        return trend

    @staticmethod
    def get_merchant_fraud_distribution(db: Session, limit: int = 20) -> List[Dict]:
        """Get fraud distribution by merchant."""
        results = db.query(
            Transaction.merchant,
            func.count(Transaction.id).label("total"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
            func.avg(Transaction.risk_score).label("avg_risk"),
        ).group_by(
            Transaction.merchant,
        ).order_by(
            func.count(Transaction.id).desc(),
        ).limit(limit).all()

        distribution = []
        for merchant, total, fraud_count, avg_risk in results:
            distribution.append({
                "merchant": merchant,
                "total_transactions": total or 0,
                "fraud_count": fraud_count or 0,
                "fraud_rate": (fraud_count / total * 100) if total > 0 else 0,
                "average_risk_score": round(avg_risk or 0.0, 3),
            })
        return distribution

    @staticmethod
    def get_transaction_type_distribution(db: Session) -> List[Dict]:
        """Get transaction distribution by type."""
        results = db.query(
            Transaction.transaction_type,
            func.count(Transaction.id).label("total"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
            func.avg(Transaction.amount).label("avg_amount"),
        ).group_by(
            Transaction.transaction_type,
        ).order_by(
            func.count(Transaction.id).desc(),
        ).all()

        distribution = []
        total = sum(t[1] for t in results)
        for transaction_type, count, fraud_count, avg_amount in results:
            distribution.append({
                "type": transaction_type,
                "count": count or 0,
                "percentage": (count / total * 100) if total > 0 else 0,
                "fraud_count": fraud_count or 0,
                "average_amount": round(avg_amount or 0.0, 2),
            })
        return distribution

    @staticmethod
    def get_amount_distribution(db: Session, bins: int = 10) -> List[Dict]:
        """Get transaction amount distribution across bins."""
        max_amount_result = db.query(func.max(Transaction.amount)).scalar()
        max_amount = max_amount_result or 10000
        bin_size = max_amount / bins

        distribution = []
        for i in range(bins):
            lower_bound = i * bin_size
            upper_bound = (i + 1) * bin_size
            count = db.query(func.count(Transaction.id)).filter(
                and_(
                    Transaction.amount >= lower_bound,
                    Transaction.amount < upper_bound,
                )
            ).scalar() or 0
            
            distribution.append({
                "bin": f"${lower_bound:,.0f} - ${upper_bound:,.0f}",
                "count": count,
                "percentage": 0,
            })

        total = sum(d["count"] for d in distribution)
        for item in distribution:
            item["percentage"] = (item["count"] / total * 100) if total > 0 else 0

        return distribution

    @staticmethod
    def get_location_fraud_stats(db: Session, limit: int = 15) -> List[Dict]:
        """Get fraud statistics by location."""
        results = db.query(
            Transaction.location,
            func.count(Transaction.id).label("total"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
            func.avg(Transaction.risk_score).label("avg_risk"),
        ).filter(
            Transaction.location.isnot(None),
            Transaction.location != "",
        ).group_by(
            Transaction.location,
        ).order_by(
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).desc(),
        ).limit(limit).all()

        stats = []
        for location, total, fraud_count, avg_risk in results:
            stats.append({
                "location": location,
                "total_transactions": total or 0,
                "fraud_count": fraud_count or 0,
                "fraud_rate": (fraud_count / total * 100) if total > 0 else 0,
                "average_risk_score": round(avg_risk or 0.0, 3),
            })
        return stats

    @staticmethod
    def get_user_activity_stats(db: Session, limit: int = 20) -> List[Dict]:
        """Get user activity statistics."""
        results = db.query(
            User.id,
            User.full_name,
            func.count(Transaction.id).label("transaction_count"),
            func.sum(Transaction.amount).label("total_amount"),
            func.sum(
                (Transaction.is_fraudulent == "fraudulent").cast(func.Integer())
            ).label("fraud_count"),
            func.avg(Transaction.risk_score).label("avg_risk"),
        ).join(
            Transaction, User.id == Transaction.user_id
        ).group_by(
            User.id, User.full_name
        ).order_by(
            func.count(Transaction.id).desc(),
        ).limit(limit).all()

        stats = []
        for user_id, full_name, trans_count, total_amount, fraud_count, avg_risk in results:
            stats.append({
                "user_id": user_id,
                "user_name": full_name,
                "transaction_count": trans_count or 0,
                "total_amount": round(total_amount or 0.0, 2),
                "fraud_count": fraud_count or 0,
                "fraud_rate": (fraud_count / trans_count * 100) if trans_count > 0 else 0,
                "average_risk_score": round(avg_risk or 0.0, 3),
            })
        return stats

    @staticmethod
    def get_risk_score_distribution(db: Session, bins: int = 10) -> List[Dict]:
        """Get distribution of risk scores."""
        results = db.query(
            func.count(FraudPrediction.id).label("count"),
            func.min(FraudPrediction.risk_score).label("min"),
            func.max(FraudPrediction.risk_score).label("max"),
        ).all()

        if not results or not results[0][1]:
            return []

        min_score = results[0][1]
        max_score = results[0][2]
        bin_size = (max_score - min_score) / bins

        distribution = []
        for i in range(bins):
            lower_bound = min_score + (i * bin_size)
            upper_bound = min_score + ((i + 1) * bin_size)
            count = db.query(func.count(FraudPrediction.id)).filter(
                and_(
                    FraudPrediction.risk_score >= lower_bound,
                    FraudPrediction.risk_score < upper_bound,
                )
            ).scalar() or 0

            distribution.append({
                "bin": f"{lower_bound:.2f} - {upper_bound:.2f}",
                "count": count,
                "percentage": 0,
            })

        total = sum(d["count"] for d in distribution)
        for item in distribution:
            item["percentage"] = (item["count"] / total * 100) if total > 0 else 0

        return distribution

    @staticmethod
    def get_device_trust_stats(db: Session) -> Dict:
        """Get device trust statistics."""
        trusted = db.query(func.count(Device.id)).filter(
            Device.is_trusted == True
        ).scalar() or 0
        untrusted = db.query(func.count(Device.id)).filter(
            Device.is_trusted == False
        ).scalar() or 0
        total = trusted + untrusted

        return {
            "trusted": {
                "count": trusted,
                "percentage": (trusted / total * 100) if total > 0 else 0,
            },
            "untrusted": {
                "count": untrusted,
                "percentage": (untrusted / total * 100) if total > 0 else 0,
            },
            "total": total,
        }

    @staticmethod
    def get_alert_statistics(db: Session, days: int = 30) -> Dict:
        """Get alert statistics for the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        total = db.query(func.count(Alert.id)).filter(
            Alert.created_at >= cutoff_date
        ).scalar() or 0
        resolved = db.query(func.count(Alert.id)).filter(
            and_(
                Alert.created_at >= cutoff_date,
                Alert.is_resolved == True,
            )
        ).scalar() or 0
        pending = total - resolved

        return {
            "total_alerts": total,
            "resolved": {
                "count": resolved,
                "percentage": (resolved / total * 100) if total > 0 else 0,
            },
            "pending": {
                "count": pending,
                "percentage": (pending / total * 100) if total > 0 else 0,
            },
        }

    @staticmethod
    def get_model_performance_stats(db: Session) -> Dict:
        """Get fraud detection model performance statistics."""
        total_predictions = db.query(func.count(FraudPrediction.id)).scalar() or 0
        fraudulent = db.query(func.count(FraudPrediction.id)).filter(
            FraudPrediction.is_fraudulent == "fraudulent"
        ).scalar() or 0
        suspicious = db.query(func.count(FraudPrediction.id)).filter(
            FraudPrediction.is_fraudulent == "suspicious"
        ).scalar() or 0
        legitimate = total_predictions - fraudulent - suspicious

        avg_risk = db.query(func.avg(FraudPrediction.risk_score)).scalar() or 0.0
        avg_confidence = db.query(func.avg(FraudPrediction.confidence_score)).scalar() or 0.0

        return {
            "total_predictions": total_predictions,
            "fraudulent": {
                "count": fraudulent,
                "percentage": (fraudulent / total_predictions * 100) if total_predictions > 0 else 0,
            },
            "suspicious": {
                "count": suspicious,
                "percentage": (suspicious / total_predictions * 100) if total_predictions > 0 else 0,
            },
            "legitimate": {
                "count": legitimate,
                "percentage": (legitimate / total_predictions * 100) if total_predictions > 0 else 0,
            },
            "average_risk_score": round(avg_risk, 3),
            "average_confidence_score": round(avg_confidence, 3),
        }
