"""Transaction endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.core.security import get_current_user
from app.core.logging import logger
from app.services.transaction_service import transaction_service
from decimal import Decimal

router = APIRouter()


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List transactions for current user.
    
    Args:
        skip: Number of results to skip
        limit: Maximum number of results
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of transactions
    """
    transactions = transaction_service.get_user_transactions(
        db,
        current_user.get('sub'),
        skip=skip,
        limit=limit
    )
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get transaction by ID.
    
    Args:
        transaction_id: Transaction ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Transaction information
    """
    transaction = transaction_service.get_transaction_by_id(db, transaction_id)
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Check authorization
    if transaction.user_id != current_user.get('sub') and current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    return transaction


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new transaction.
    
    Args:
        transaction_data: Transaction data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created transaction
    """
    transaction = transaction_service.create_transaction(
        db=db,
        user_id=current_user.get('sub'),
        amount=transaction_data.amount,
        currency=transaction_data.currency,
        merchant_name=transaction_data.merchant_name,
        transaction_type=transaction_data.transaction_type,
        device_id=transaction_data.device_id,
        merchant_category=transaction_data.merchant_category,
        description=transaction_data.description,
        transaction_date=transaction_data.transaction_date
    )
    
    return transaction


@router.get("/user/{user_id}", response_model=List[TransactionResponse])
async def get_user_transactions(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get transactions for a specific user.
    
    Args:
        user_id: User ID
        skip: Number of results to skip
        limit: Maximum number of results
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of transactions
    """
    # Check authorization
    if user_id != current_user.get('sub') and current_user.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    transactions = transaction_service.get_user_transactions(
        db,
        user_id,
        skip=skip,
        limit=limit
    )
    return transactions
