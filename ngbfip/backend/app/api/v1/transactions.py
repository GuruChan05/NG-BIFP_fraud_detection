from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.transaction import TransactionResponse, TransactionCreate

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implement list transactions
    pass

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    # TODO: Implement get transaction
    pass

@router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # TODO: Implement create transaction
    pass
