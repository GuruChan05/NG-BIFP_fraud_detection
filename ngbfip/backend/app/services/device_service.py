"""Device service for device management."""
import uuid
from sqlalchemy.orm import Session
from app.db.models.device import Device
from app.core.audit import audit_logger
from app.core.logging import logger
from typing import List, Optional
from fastapi import HTTPException, status


class DeviceService:
    """Service for device management operations."""
    
    @staticmethod
    def create_device(
        db: Session,
        user_id: str,
        device_name: str,
        device_type: str,
        device_fingerprint: str,
        os: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Device:
        """Create a new device.
        
        Args:
            db: Database session
            user_id: User ID
            device_name: Device name
            device_type: Device type
            device_fingerprint: Device fingerprint
            os: Operating system
            ip_address: IP address
            
        Returns:
            Created device
        """
        try:
            device = Device(
                id=str(uuid.uuid4()),
                user_id=user_id,
                device_name=device_name,
                device_type=device_type,
                device_fingerprint=device_fingerprint,
                os=os,
                ip_address=ip_address,
                trust_score=0.5,
                is_trusted=False
            )
            
            db.add(device)
            db.commit()
            db.refresh(device)
            
            logger.info(f"Device created: {device.id} for user {user_id}")
            audit_logger.log_action(
                user_id=user_id,
                action="CREATE_DEVICE",
                resource_type="DEVICE",
                resource_id=device.id,
                details={"device_name": device_name, "device_type": device_type}
            )
            
            return device
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating device: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating device"
            )
    
    @staticmethod
    def get_device_by_id(db: Session, device_id: str) -> Optional[Device]:
        """Get device by ID.
        
        Args:
            db: Database session
            device_id: Device ID
            
        Returns:
            Device if found, None otherwise
        """
        return db.query(Device).filter(Device.id == device_id).first()
    
    @staticmethod
    def get_user_devices(db: Session, user_id: str) -> List[Device]:
        """Get all devices for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of devices
        """
        return db.query(Device).filter(
            Device.user_id == user_id,
            Device.is_active == True
        ).all()
    
    @staticmethod
    def update_device_trust(
        db: Session,
        device_id: str,
        is_trusted: bool,
        trust_score: Optional[float] = None,
        trust_level: Optional[str] = None
    ) -> Optional[Device]:
        """Update device trust status.
        
        Args:
            db: Database session
            device_id: Device ID
            is_trusted: Trust status
            trust_score: Trust score (0-1)
            trust_level: Trust level
            
        Returns:
            Updated device
        """
        device = db.query(Device).filter(Device.id == device_id).first()
        
        if not device:
            return None
        
        try:
            device.is_trusted = is_trusted
            if trust_score is not None:
                device.trust_score = trust_score
            if trust_level is not None:
                device.trust_level = trust_level
            
            db.commit()
            db.refresh(device)
            
            audit_logger.log_action(
                user_id=device.user_id,
                action="UPDATE_DEVICE_TRUST",
                resource_type="DEVICE",
                resource_id=device_id,
                details={"is_trusted": is_trusted, "trust_score": trust_score}
            )
            
            return device
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating device trust: {str(e)}")
            raise
    
    @staticmethod
    def mark_device_compromised(
        db: Session,
        device_id: str
    ) -> Optional[Device]:
        """Mark device as compromised.
        
        Args:
            db: Database session
            device_id: Device ID
            
        Returns:
            Updated device
        """
        device = db.query(Device).filter(Device.id == device_id).first()
        
        if not device:
            return None
        
        try:
            device.is_compromised = True
            device.is_trusted = False
            device.trust_score = 0.0
            
            db.commit()
            db.refresh(device)
            
            audit_logger.log_action(
                user_id=device.user_id,
                action="MARK_COMPROMISED",
                resource_type="DEVICE",
                resource_id=device_id
            )
            
            return device
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error marking device compromised: {str(e)}")
            raise


device_service = DeviceService()
