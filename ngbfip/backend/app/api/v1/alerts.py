"""Alert endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.schemas.alert import AlertResponse, AlertResolve
from app.core.security import get_current_user
from app.core.logging import logger
from app.services.alert_service import alert_service

router = APIRouter()


@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    severity: str = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List alerts.
    
    Args:
        skip: Number of results to skip
        limit: Maximum number of results
        status: Filter by status
        severity: Filter by severity
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of alerts
    """
    if severity:
        alerts = alert_service.get_alerts_by_severity(db, severity, skip=skip, limit=limit)
    else:
        alerts = alert_service.get_open_alerts(db, skip=skip, limit=limit)
    
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get alert by ID.
    
    Args:
        alert_id: Alert ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Alert information
    """
    alert = alert_service.get_alert_by_id(db, alert_id)
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert


@router.put("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: str,
    resolve_data: AlertResolve,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resolve an alert.
    
    Args:
        alert_id: Alert ID
        resolve_data: Resolution data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated alert
    """
    alert = alert_service.resolve_alert(
        db,
        alert_id,
        resolve_data.status,
        current_user.get('sub'),
        resolve_data.resolution_notes
    )
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    return alert
