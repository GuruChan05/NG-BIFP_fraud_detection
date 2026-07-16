from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.device import DeviceResponse, DeviceCreate

router = APIRouter()

@router.get("/", response_model=List[DeviceResponse])
async def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.db.models.device import Device
    devices = db.query(Device).offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str, db: Session = Depends(get_db)):
    from app.db.models.device import Device
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/", response_model=DeviceResponse)
async def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    from app.db.models.device import Device
    db_device = Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
