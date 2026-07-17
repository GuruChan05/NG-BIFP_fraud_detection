from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.transaction import (
    TransactionResponse, TransactionCreate, TransactionUpdate, TransactionListResponse
)
from app.services.transaction import TransactionService
from app.services.fraud_prediction import FraudPredictionService
from app.db.models.user import User
from app.db.models.transaction import Transaction
from app.api.deps import get_current_active_user
from typing import Optional, List
import csv
import io

router = APIRouter()


@router.get("/", response_model=TransactionListResponse)
async def list_transactions(
    skip: int = 0,
    limit: int = 20,
    user_id: Optional[int] = None,
    merchant: Optional[str] = None,
    is_fraudulent: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List transactions with filters and pagination."""
    transactions, total = TransactionService.list_transactions(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        merchant=merchant,
        is_fraudulent=is_fraudulent,
        min_amount=min_amount,
        max_amount=max_amount
    )
    
    return {
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": transactions
    }


@router.get("/search")
async def search_transactions(
    q: str,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Search transactions by merchant or other fields."""
    transactions = TransactionService.search_transactions(db, q, limit)
    return transactions


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new transaction."""
    new_transaction = TransactionService.create_transaction(
        db=db,
        **transaction.dict()
    )
    
    # Generate fraud prediction
    prediction = FraudPredictionService.predict_fraud(new_transaction)
    new_transaction.risk_score = prediction['risk_score']
    new_transaction.is_fraudulent = prediction['prediction']
    db.commit()
    
    return new_transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get transaction by ID."""
    transaction = TransactionService.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update transaction."""
    transaction = TransactionService.update_transaction(
        db=db,
        transaction_id=transaction_id,
        **transaction_data.dict(exclude_unset=True)
    )
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete transaction."""
    success = TransactionService.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}


@router.get("/user/{user_id}")
async def get_user_transactions(
    user_id: int,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get transactions for a specific user."""
    transactions = TransactionService.get_user_transactions(db, user_id, limit)
    return transactions


@router.get("/fraud/list")
async def get_fraud_transactions(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get fraudulent transactions."""
    transactions = TransactionService.get_fraud_transactions(db, limit)
    return transactions


@router.get("/high-risk/list")
async def get_high_risk_transactions(
    threshold: float = 70,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get high-risk transactions."""
    transactions = TransactionService.get_high_risk_transactions(db, threshold, limit)
    return transactions


@router.post("/import/csv")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Import transactions from CSV file."""
    try:
        contents = await file.read()
        stream = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(stream)
        
        count = 0
        for row in csv_reader:
            transaction = TransactionService.create_transaction(
                db=db,
                user_id=int(row.get('user_id', 1)),
                amount=float(row.get('amount', 0)),
                transaction_type=row.get('transaction_type', ''),
                merchant=row.get('merchant', ''),
                merchant_category=row.get('merchant_category'),
                location=row.get('location'),
                device_id=row.get('device_id'),
                is_fraudulent=row.get('is_fraudulent', 'Unknown')
            )
            count += 1
        
        return {"message": f"Imported {count} transactions successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


@router.get("/export/csv")
async def export_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Export transactions as CSV file."""
    transactions = db.query(Transaction).all()
    
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=['id', 'user_id', 'amount', 'transaction_type', 'merchant', 'risk_score', 'is_fraudulent', 'created_at']
    )
    writer.writeheader()
    
    for tx in transactions:
        writer.writerow({
            'id': tx.id,
            'user_id': tx.user_id,
            'amount': tx.amount,
            'transaction_type': tx.transaction_type,
            'merchant': tx.merchant,
            'risk_score': tx.risk_score,
            'is_fraudulent': tx.is_fraudulent,
            'created_at': tx.created_at
        })
    
    return {"csv": output.getvalue()}
