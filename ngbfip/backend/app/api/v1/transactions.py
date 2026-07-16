"""Transaction API endpoints with CRUD operations."""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.api.deps import get_current_active_user
from app.db.models.user import User
from app.services.transaction import TransactionService
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
    TransactionStats,
    BulkImportResponse,
)

router = APIRouter()


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new transaction.
    
    Validates the transaction data and creates it in the database.
    """
    try:
        is_valid, errors = TransactionService.validate_transaction(transaction)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": errors},
            )
        
        db_transaction = TransactionService.create_transaction(db, transaction)
        return TransactionResponse.from_orm(db_transaction)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating transaction: {str(e)}",
        )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a transaction by ID.
    """
    try:
        db_transaction = TransactionService.get_transaction(db, transaction_id)
        if not db_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        return TransactionResponse.from_orm(db_transaction)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transaction: {str(e)}",
        )


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a transaction.
    """
    try:
        db_transaction = TransactionService.update_transaction(
            db, transaction_id, transaction
        )
        if not db_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        return TransactionResponse.from_orm(db_transaction)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating transaction: {str(e)}",
        )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a transaction.
    """
    try:
        success = TransactionService.delete_transaction(db, transaction_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting transaction: {str(e)}",
        )


@router.get("/", response_model=TransactionListResponse)
async def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    fraud_status: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    merchant: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List transactions with filtering, searching, and pagination.
    
    Query parameters:
    - page: Page number (default: 1)
    - page_size: Number of items per page (default: 20, max: 100)
    - user_id: Filter by user ID
    - fraud_status: Filter by fraud status (unknown, legitimate, fraudulent)
    - min_amount: Filter by minimum amount
    - max_amount: Filter by maximum amount
    - merchant: Filter by merchant name (substring match)
    - search: Search in merchant, location, device_id
    - sort_by: Sort field (created_at, amount, risk_score)
    - sort_order: Sort order (asc, desc)
    """
    try:
        transactions, total = TransactionService.list_transactions(
            db,
            page=page,
            page_size=page_size,
            user_id=user_id,
            fraud_status=fraud_status,
            min_amount=min_amount,
            max_amount=max_amount,
            merchant=merchant,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        
        total_pages = (total + page_size - 1) // page_size
        
        return TransactionListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            data=[TransactionResponse.from_orm(t) for t in transactions],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transactions: {str(e)}",
        )


@router.get("/search/query", response_model=List[TransactionResponse])
async def search_transactions(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Search transactions by merchant, location, or device ID.
    """
    try:
        transactions = TransactionService.search_transactions(db, q)
        return [TransactionResponse.from_orm(t) for t in transactions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching transactions: {str(e)}",
        )


@router.get("/user/{user_id}/history", response_model=List[TransactionResponse])
async def get_user_transaction_history(
    user_id: int,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get transaction history for a specific user.
    """
    try:
        transactions = TransactionService.get_transaction_history(
            db, user_id=user_id, limit=limit
        )
        return [TransactionResponse.from_orm(t) for t in transactions]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching transaction history: {str(e)}",
        )


@router.get("/stats/summary", response_model=TransactionStats)
async def get_transaction_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get transaction statistics.
    """
    try:
        stats = TransactionService.get_statistics(db)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}",
        )


@router.post("/import/csv", response_model=BulkImportResponse)
async def import_transactions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Import transactions from a CSV file.
    
    Expected CSV columns:
    - user_id (int)
    - amount (float)
    - transaction_type (debit, credit, transfer)
    - merchant (string)
    - merchant_category (optional)
    - location (optional)
    - device_id (optional)
    - risk_score (optional, float 0-1)
    - is_fraudulent (optional, unknown/legitimate/fraudulent)
    """
    try:
        if file.content_type != "text/csv":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a CSV file",
            )
        
        content = await file.read()
        csv_content = content.decode("utf-8")
        
        results = TransactionService.import_transactions_from_csv(db, csv_content)
        
        return BulkImportResponse(
            total_imported=results["total_imported"],
            successful=results["successful"],
            failed=results["failed"],
            errors=results["errors"][:10],  # Return first 10 errors
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing transactions: {str(e)}",
        )


@router.get("/export/csv")
async def export_transactions_csv(
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Export transactions to CSV format.
    
    Optional: Filter by user_id
    """
    try:
        csv_content = TransactionService.export_transactions_to_csv(
            db, user_id=user_id
        )
        
        return {
            "content": csv_content,
            "filename": f"transactions_{current_user.id}.csv",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting transactions: {str(e)}",
        )
