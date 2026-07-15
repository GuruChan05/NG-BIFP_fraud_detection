"""Dashboard endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.transaction_service import transaction_service

router = APIRouter()


@router.get("/overview")
async def dashboard_overview(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard overview.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dashboard overview data
    """
    # Get flagged transactions
    flagged = transaction_service.get_flagged_transactions(db, limit=5)
    
    return {
        "user_id": current_user.get('sub'),
        "flagged_transactions_count": len(flagged),
        "recent_alerts": 3,
        "average_risk_score": 0.35,
        "status": "Active"
    }


@router.get("/statistics")
async def dashboard_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed dashboard statistics.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Detailed statistics
    """
    return {
        "transactions": {
            "total": 156,
            "today": 12,
            "flagged": 5
        },
        "risk": {
            "low": 145,
            "medium": 8,
            "high": 3,
            "critical": 0
        },
        "devices": {
            "total": 4,
            "trusted": 2,
            "untrusted": 2
        },
        "alerts": {
            "open": 3,
            "resolved": 12,
            "dismissed": 4
        }
    }
