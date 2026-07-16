from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.transaction import TransactionResponse, TransactionCreate

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.db.models.transaction import Transaction
    transactions = db.query(Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    from app.db.models.transaction import Transaction
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    from app.db.models.transaction import Transaction
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
