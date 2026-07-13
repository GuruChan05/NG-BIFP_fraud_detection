from sqlalchemy.orm import Session
from app.db.models.transaction import Transaction
from typing import List

class TransactionService:
    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int):
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def list_transactions(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        query = db.query(Transaction)
        if user_id:
            query = query.filter(Transaction.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_transaction(db: Session, transaction_data: dict):
        transaction = Transaction(**transaction_data)
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
