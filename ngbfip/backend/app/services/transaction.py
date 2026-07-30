from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from app.db.models.transaction import Transaction
from app.db.models.fraud_prediction import FraudPrediction
from typing import Optional, List
from datetime import datetime


class TransactionService:
    @staticmethod
    def create_transaction(db: Session, **kwargs) -> Transaction:
        """Create a new transaction."""
        transaction = Transaction(**kwargs)
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    @staticmethod
    def list_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        user_id: Optional[int] = None,
        merchant: Optional[str] = None,
        is_fraudulent: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None
    ) -> tuple:
        """List transactions with filters and pagination."""
        query = db.query(Transaction)
        
        if user_id:
            query = query.filter(Transaction.user_id == user_id)
        if merchant:
            query = query.filter(Transaction.merchant.ilike(f"%{merchant}%"))
        if is_fraudulent:
            query = query.filter(Transaction.is_fraudulent == is_fraudulent)
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        
        total = query.count()
        transactions = query.order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()
        
        return transactions, total
    
    @staticmethod
    def search_transactions(db: Session, query_str: str, limit: int = 20) -> List[Transaction]:
        """Search transactions by merchant or other fields."""
        return db.query(Transaction).filter(
            or_(
                Transaction.merchant.ilike(f"%{query_str}%"),
                Transaction.transaction_type.ilike(f"%{query_str}%")
            )
        ).limit(limit).all()
    
    @staticmethod
    def update_transaction(db: Session, transaction_id: int, **kwargs) -> Optional[Transaction]:
        """Update transaction."""
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            return None
        
        for key, value in kwargs.items():
            if value is not None and hasattr(transaction, key):
                setattr(transaction, key, value)
        
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> bool:
        """Delete transaction."""
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            return False
        
        db.delete(transaction)
        db.commit()
        return True
    
    @staticmethod
    def get_user_transactions(db: Session, user_id: int, limit: int = 50) -> List[Transaction]:
        """Get transactions for a specific user."""
        return db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_fraud_transactions(db: Session, limit: int = 50) -> List[Transaction]:
        """Get fraudulent transactions."""
        return db.query(Transaction).filter(
            Transaction.is_fraudulent == 'Yes'
        ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_high_risk_transactions(db: Session, risk_threshold: float = 70, limit: int = 50) -> List[Transaction]:
        """Get high-risk transactions."""
        return db.query(Transaction).filter(
            Transaction.risk_score >= risk_threshold
        ).order_by(Transaction.risk_score.desc()).limit(limit).all()
