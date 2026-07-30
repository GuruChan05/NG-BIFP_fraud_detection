from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.db.models.transaction import Transaction
from app.db.models.user import User
from app.db.models.alert import Alert
from app.db.models.fraud_prediction import FraudPrediction
from app.db.models.device import Device


class DashboardService:
    @staticmethod
    def get_overview(db: Session) -> dict:
        """Get comprehensive dashboard overview statistics."""
        
        # Total transactions
        total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
        
        # Fraud cases
        fraud_cases = db.query(func.count(Transaction.id)).filter(
            Transaction.is_fraudulent == 'Yes'
        ).scalar() or 0
        
        # Active users (logged in last 24 hours)
        active_users = db.query(func.count(User.id)).filter(
            User.last_login >= datetime.utcnow() - timedelta(days=1),
            User.is_active == True
        ).scalar() or 0
        
        # Today's activity
        today = datetime.utcnow().date()
        todays_activity = db.query(func.count(Transaction.id)).filter(
            func.date(Transaction.created_at) == today
        ).scalar() or 0
        
        # Average risk score
        avg_risk = db.query(func.avg(Transaction.risk_score)).scalar() or 0
        
        # Trusted devices
        trusted_devices = db.query(func.count(Device.id)).filter(
            Device.is_trusted == True
        ).scalar() or 0
        
        # High risk transactions
        high_risk = db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score >= 70
        ).scalar() or 0
        
        # Resolved alerts
        resolved_alerts = db.query(func.count(Alert.id)).filter(
            Alert.status == 'resolved'
        ).scalar() or 0
        
        return {
            'total_transactions': total_transactions,
            'fraud_cases': fraud_cases,
            'active_users': active_users,
            'todays_activity': todays_activity,
            'average_risk_score': round(float(avg_risk), 2),
            'trusted_devices': trusted_devices,
            'high_risk_transactions': high_risk,
            'resolved_alerts': resolved_alerts,
            'fraud_percentage': round((fraud_cases / total_transactions * 100), 2) if total_transactions > 0 else 0
        }
    
    @staticmethod
    def get_summary_stats(db: Session) -> dict:
        """Get detailed summary statistics."""
        
        # Transaction statistics
        total_amount = db.query(func.sum(Transaction.amount)).scalar() or 0
        avg_amount = db.query(func.avg(Transaction.amount)).scalar() or 0
        max_amount = db.query(func.max(Transaction.amount)).scalar() or 0
        min_amount = db.query(func.min(Transaction.amount)).scalar() or 0
        
        # User statistics
        total_users = db.query(func.count(User.id)).scalar() or 0
        active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
        admin_users = db.query(func.count(User.id)).filter(User.is_admin == True).scalar() or 0
        
        # Risk distribution
        low_risk = db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score < 30
        ).scalar() or 0
        medium_risk = db.query(func.count(Transaction.id)).filter(
            and_(Transaction.risk_score >= 30, Transaction.risk_score < 70)
        ).scalar() or 0
        high_risk = db.query(func.count(Transaction.id)).filter(
            Transaction.risk_score >= 70
        ).scalar() or 0
        
        return {
            'transactions': {
                'total_amount': float(total_amount),
                'average_amount': round(float(avg_amount), 2),
                'max_amount': float(max_amount),
                'min_amount': float(min_amount)
            },
            'users': {
                'total': total_users,
                'active': active_users,
                'admins': admin_users
            },
            'risk_distribution': {
                'low': low_risk,
                'medium': medium_risk,
                'high': high_risk
            }
        }
    
    @staticmethod
    def get_recent_transactions(db: Session, limit: int = 10) -> list:
        """Get recent transactions with user info."""
        transactions = db.query(Transaction).order_by(
            Transaction.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for tx in transactions:
            result.append({
                'id': tx.id,
                'user_id': tx.user_id,
                'amount': float(tx.amount),
                'transaction_type': tx.transaction_type,
                'merchant': tx.merchant,
                'risk_score': float(tx.risk_score),
                'is_fraudulent': tx.is_fraudulent,
                'created_at': tx.created_at.isoformat()
            })
        
        return result
    
    @staticmethod
    def get_daily_summary(db: Session, days: int = 7) -> list:
        """Get daily transaction summary for the past N days."""
        result = []
        
        for i in range(days):
            date = datetime.utcnow().date() - timedelta(days=i)
            
            count = db.query(func.count(Transaction.id)).filter(
                func.date(Transaction.created_at) == date
            ).scalar() or 0
            
            fraud_count = db.query(func.count(Transaction.id)).filter(
                func.date(Transaction.created_at) == date,
                Transaction.is_fraudulent == 'Yes'
            ).scalar() or 0
            
            amount = db.query(func.sum(Transaction.amount)).filter(
                func.date(Transaction.created_at) == date
            ).scalar() or 0
            
            result.append({
                'date': date.isoformat(),
                'transactions': count,
                'fraud_count': fraud_count,
                'total_amount': float(amount),
                'fraud_percentage': round((fraud_count / count * 100), 2) if count > 0 else 0
            })
        
        return list(reversed(result))
    
    @staticmethod
    def get_fraud_trends(db: Session, days: int = 30) -> list:
        """Get fraud trends for the past N days."""
        result = []
        
        for i in range(days):
            date = datetime.utcnow().date() - timedelta(days=i)
            
            fraud_count = db.query(func.count(Transaction.id)).filter(
                func.date(Transaction.created_at) == date,
                Transaction.is_fraudulent == 'Yes'
            ).scalar() or 0
            
            total_count = db.query(func.count(Transaction.id)).filter(
                func.date(Transaction.created_at) == date
            ).scalar() or 0
            
            result.append({
                'date': date.isoformat(),
                'fraud_count': fraud_count,
                'total_count': total_count,
                'fraud_rate': round((fraud_count / total_count * 100), 2) if total_count > 0 else 0
            })
        
        return list(reversed(result))
    
    @staticmethod
    def get_risk_distribution(db: Session) -> dict:
        """Get risk score distribution."""
        total = db.query(func.count(Transaction.id)).scalar() or 1
        
        return {
            'very_low': db.query(func.count(Transaction.id)).filter(
                Transaction.risk_score < 20
            ).scalar() or 0,
            'low': db.query(func.count(Transaction.id)).filter(
                and_(Transaction.risk_score >= 20, Transaction.risk_score < 40)
            ).scalar() or 0,
            'medium': db.query(func.count(Transaction.id)).filter(
                and_(Transaction.risk_score >= 40, Transaction.risk_score < 60)
            ).scalar() or 0,
            'high': db.query(func.count(Transaction.id)).filter(
                and_(Transaction.risk_score >= 60, Transaction.risk_score < 80)
            ).scalar() or 0,
            'very_high': db.query(func.count(Transaction.id)).filter(
                Transaction.risk_score >= 80
            ).scalar() or 0,
            'total': total
        }
