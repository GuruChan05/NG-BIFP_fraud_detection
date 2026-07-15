"""Transaction service for transaction management."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.transaction import Transaction
from app.core.audit import audit_logger
from app.core.logging import logger
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status


class TransactionService:
    """Service for transaction management operations."""
    
    @staticmethod
    def create_transaction(
        db: Session,
        user_id: str,
        amount: float,
        currency: str,
        merchant_name: str,
        transaction_type: str,
        device_id: Optional[str] = None,
        merchant_category: Optional[str] = None,
        description: Optional[str] = None,
        transaction_date: Optional[datetime] = None
    ) -> Transaction:
        """Create a new transaction.
        
        Args:
            db: Database session
            user_id: User ID
            amount: Transaction amount
            currency: Currency code
            merchant_name: Merchant name
            transaction_type: Type of transaction
            device_id: Device ID (optional)
            merchant_category: Merchant category
            description: Transaction description
            transaction_date: Transaction date
            
        Returns:
            Created transaction
        """
        try:
            transaction = Transaction(
                id=str(uuid.uuid4()),
                user_id=user_id,
                device_id=device_id,
                amount=amount,
                currency=currency,
                merchant_name=merchant_name,
                merchant_category=merchant_category,
                transaction_type=transaction_type,
                description=description,
                transaction_date=transaction_date or datetime.utcnow(),
                risk_score=0.0,
                status="pending"
            )
            
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            
            logger.info(f"Transaction created: {transaction.id} for user {user_id}")
            audit_logger.log_action(
                user_id=user_id,
                action="CREATE_TRANSACTION",
                resource_type="TRANSACTION",
                resource_id=transaction.id,
                details={"amount": float(amount), "merchant": merchant_name}
            )
            
            return transaction
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating transaction: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating transaction"
            )
    
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID.
        
        Args:
            db: Database session
            transaction_id: Transaction ID
            
        Returns:
            Transaction if found, None otherwise
        """
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    @staticmethod
    def get_user_transactions(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions for a user.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of results to skip
            limit: Maximum number of results
            
        Returns:
            List of transactions
        """
        return db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(desc(Transaction.transaction_date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_transaction_risk(
        db: Session,
        transaction_id: str,
        risk_score: float,
        risk_level: str,
        is_flagged: bool,
        anomaly_score: Optional[float] = None,
        device_trust_score: Optional[float] = None
    ) -> Optional[Transaction]:
        """Update transaction risk information.
        
        Args:
            db: Database session
            transaction_id: Transaction ID
            risk_score: Risk score (0-1)
            risk_level: Risk level
            is_flagged: Whether transaction is flagged
            anomaly_score: Anomaly detection score
            device_trust_score: Device trust score
            
        Returns:
            Updated transaction
        """
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        
        if not transaction:
            return None
        
        try:
            transaction.risk_score = risk_score
            transaction.risk_level = risk_level
            transaction.is_flagged = is_flagged
            transaction.anomaly_score = anomaly_score
            transaction.device_trust_score = device_trust_score
            
            db.commit()
            db.refresh(transaction)
            
            audit_logger.log_transaction_analysis(
                user_id=transaction.user_id,
                transaction_id=transaction_id,
                risk_score=risk_score,
                risk_level=risk_level
            )
            
            return transaction
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating transaction risk: {str(e)}")
            raise
    
    @staticmethod
    def update_transaction_status(
        db: Session,
        transaction_id: str,
        status: str
    ) -> Optional[Transaction]:
        """Update transaction status.
        
        Args:
            db: Database session
            transaction_id: Transaction ID
            status: New status
            
        Returns:
            Updated transaction
        """
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        
        if not transaction:
            return None
        
        try:
            transaction.status = status
            db.commit()
            db.refresh(transaction)
            
            return transaction
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating transaction status: {str(e)}")
            raise
    
    @staticmethod
    def get_flagged_transactions(
        db: Session,
        skip: int = 0,
        limit: int = 50
    ) -> List[Transaction]:
        """Get all flagged transactions.
        
        Args:
            db: Database session
            skip: Number of results to skip
            limit: Maximum number of results
            
        Returns:
            List of flagged transactions
        """
        return db.query(Transaction).filter(
            Transaction.is_flagged == True
        ).order_by(desc(Transaction.created_at)).offset(skip).limit(limit).all()


transaction_service = TransactionService()
