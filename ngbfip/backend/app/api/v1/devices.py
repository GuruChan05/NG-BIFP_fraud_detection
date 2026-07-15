"""Device endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceTrustUpdate
from app.core.security import get_current_user
from app.core.logging import logger
from app.services.device_service import device_service

router = APIRouter()


@router.get("/", response_model=List[DeviceResponse])
async def list_devices(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List devices for current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List of devices
    """
    devices = device_service.get_user_devices(db, current_user.get('sub'))
    return devices


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device by ID.
    
    Args:
        device_id: Device ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Device information
    """
    device = device_service.get_device_by_id(db, device_id)
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Check authorization
    if device.user_id != current_user.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    return device


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(
    device_data: DeviceCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register a new device.
    
    Args:
        device_data: Device registration data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Registered device
    """
    device = device_service.create_device(
        db=db,
        user_id=current_user.get('sub'),
        device_name=device_data.device_name,
        device_type=device_data.device_type,
        device_fingerprint=device_data.device_fingerprint,
        os=device_data.os,
        ip_address=device_data.ip_address
    )
    
    return device


@router.put("/{device_id}/trust", response_model=DeviceResponse)
async def update_device_trust(
    device_id: str,
    trust_data: DeviceTrustUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update device trust status.
    
    Args:
        device_id: Device ID
        trust_data: Trust update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Updated device
    """
    device = device_service.get_device_by_id(db, device_id)
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Check authorization
    if device.user_id != current_user.get('sub'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    updated_device = device_service.update_device_trust(
        db,
        device_id,
        trust_data.is_trusted,
        trust_level=trust_data.trust_level
    )
    
    return updated_device
