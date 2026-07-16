"""Transaction service with business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from app.db.models.transaction import Transaction
from app.db.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionStats,
)
import csv
from io import StringIO


class TransactionService:
    """Service for transaction management."""

    @staticmethod
    def create_transaction(db: Session, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        db_transaction = Transaction(
            user_id=transaction_data.user_id,
            amount=transaction_data.amount,
            transaction_type=transaction_data.transaction_type,
            merchant=transaction_data.merchant,
            merchant_category=transaction_data.merchant_category,
            location=transaction_data.location,
            device_id=transaction_data.device_id,
            risk_score=transaction_data.risk_score,
            is_fraudulent=transaction_data.is_fraudulent,
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def get_transaction(db: Session, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def update_transaction(
        db: Session, transaction_id: int, transaction_data: TransactionUpdate
    ) -> Optional[Transaction]:
        """Update a transaction."""
        db_transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        if not db_transaction:
            return None

        update_data = transaction_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)

        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def delete_transaction(db: Session, transaction_id: int) -> bool:
        """Delete a transaction."""
        db_transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        if not db_transaction:
            return False

        db.delete(db_transaction)
        db.commit()
        return True

    @staticmethod
    def list_transactions(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        user_id: Optional[int] = None,
        fraud_status: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        merchant: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> Tuple[List[Transaction], int]:
        """List transactions with filtering and pagination."""
        query = db.query(Transaction)

        # Apply filters
        if user_id:
            query = query.filter(Transaction.user_id == user_id)
        
        if fraud_status:
            query = query.filter(Transaction.is_fraudulent == fraud_status)
        
        if min_amount is not None:
            query = query.filter(Transaction.amount >= min_amount)
        
        if max_amount is not None:
            query = query.filter(Transaction.amount <= max_amount)
        
        if merchant:
            query = query.filter(Transaction.merchant.ilike(f"%{merchant}%"))
        
        if search:
            query = query.filter(
                or_(
                    Transaction.merchant.ilike(f"%{search}%"),
                    Transaction.location.ilike(f"%{search}%"),
                    Transaction.device_id.ilike(f"%{search}%"),
                )
            )

        # Get total count
        total = query.count()

        # Apply sorting
        if sort_by == "created_at":
            if sort_order == "asc":
                query = query.order_by(Transaction.created_at.asc())
            else:
                query = query.order_by(Transaction.created_at.desc())
        elif sort_by == "amount":
            if sort_order == "asc":
                query = query.order_by(Transaction.amount.asc())
            else:
                query = query.order_by(Transaction.amount.desc())
        elif sort_by == "risk_score":
            if sort_order == "asc":
                query = query.order_by(Transaction.risk_score.asc())
            else:
                query = query.order_by(Transaction.risk_score.desc())

        # Apply pagination
        skip = (page - 1) * page_size
        transactions = query.offset(skip).limit(page_size).all()

        return transactions, total

    @staticmethod
    def search_transactions(db: Session, search_term: str) -> List[Transaction]:
        """Search transactions by merchant, location, or device ID."""
        return db.query(Transaction).filter(
            or_(
                Transaction.merchant.ilike(f"%{search_term}%"),
                Transaction.location.ilike(f"%{search_term}%"),
                Transaction.device_id.ilike(f"%{search_term}%"),
            )
        ).limit(50).all()

    @staticmethod
    def get_transaction_history(
        db: Session, user_id: int, limit: int = 50
    ) -> List[Transaction]:
        """Get transaction history for a specific user."""
        return db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_statistics(db: Session) -> TransactionStats:
        """Get transaction statistics."""
        total_count = db.query(func.count(Transaction.id)).scalar() or 0
        total_amount = db.query(func.sum(Transaction.amount)).scalar() or 0.0
        avg_amount = db.query(func.avg(Transaction.amount)).scalar() or 0.0
        fraud_count = db.query(func.count(Transaction.id)).filter(
            Transaction.is_fraudulent == "fraudulent"
        ).scalar() or 0
        legitimate_count = db.query(func.count(Transaction.id)).filter(
            Transaction.is_fraudulent == "legitimate"
        ).scalar() or 0
        unknown_count = db.query(func.count(Transaction.id)).filter(
            Transaction.is_fraudulent == "unknown"
        ).scalar() or 0

        fraud_percentage = (fraud_count / total_count * 100) if total_count > 0 else 0.0

        return TransactionStats(
            total_transactions=total_count,
            total_amount=round(total_amount, 2),
            average_amount=round(avg_amount, 2),
            fraud_count=fraud_count,
            fraud_percentage=round(fraud_percentage, 2),
            legitimate_count=legitimate_count,
            unknown_count=unknown_count,
        )

    @staticmethod
    def import_transactions_from_csv(
        db: Session, csv_content: str
    ) -> Dict[str, any]:
        """Import transactions from CSV content."""
        results = {
            "total_imported": 0,
            "successful": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            csv_reader = csv.DictReader(StringIO(csv_content))
            for row_num, row in enumerate(csv_reader, start=2):
                try:
                    transaction_data = TransactionCreate(
                        user_id=int(row["user_id"]),
                        amount=float(row["amount"]),
                        transaction_type=row["transaction_type"],
                        merchant=row["merchant"],
                        merchant_category=row.get("merchant_category"),
                        location=row.get("location"),
                        device_id=row.get("device_id"),
                        risk_score=float(row.get("risk_score", 0.0)),
                        is_fraudulent=row.get("is_fraudulent", "unknown"),
                    )
                    TransactionService.create_transaction(db, transaction_data)
                    results["successful"] += 1
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append(f"Row {row_num}: {str(e)}")
                
                results["total_imported"] += 1
        except Exception as e:
            results["errors"].append(f"CSV parsing error: {str(e)}")

        return results

    @staticmethod
    def export_transactions_to_csv(
        db: Session, user_id: Optional[int] = None
    ) -> str:
        """Export transactions to CSV format."""
        query = db.query(Transaction)
        if user_id:
            query = query.filter(Transaction.user_id == user_id)
        
        transactions = query.all()

        output = StringIO()
        fieldnames = [
            "id",
            "user_id",
            "amount",
            "transaction_type",
            "merchant",
            "merchant_category",
            "location",
            "device_id",
            "risk_score",
            "is_fraudulent",
            "created_at",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for transaction in transactions:
            writer.writerow({
                "id": transaction.id,
                "user_id": transaction.user_id,
                "amount": transaction.amount,
                "transaction_type": transaction.transaction_type,
                "merchant": transaction.merchant,
                "merchant_category": transaction.merchant_category,
                "location": transaction.location,
                "device_id": transaction.device_id,
                "risk_score": transaction.risk_score,
                "is_fraudulent": transaction.is_fraudulent,
                "created_at": transaction.created_at.isoformat(),
            })

        return output.getvalue()

    @staticmethod
    def validate_transaction(transaction_data: TransactionCreate) -> Tuple[bool, List[str]]:
        """Validate transaction data."""
        errors = []

        if transaction_data.amount <= 0:
            errors.append("Amount must be greater than 0")
        
        if transaction_data.amount > 1000000:
            errors.append("Amount exceeds maximum allowed value")
        
        if not transaction_data.merchant:
            errors.append("Merchant is required")
        
        if transaction_data.risk_score < 0 or transaction_data.risk_score > 1:
            errors.append("Risk score must be between 0 and 1")
        
        if transaction_data.user_id <= 0:
            errors.append("Invalid user ID")

        return len(errors) == 0, errors
