from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.schemas.device import DeviceResponse, DeviceCreate

router = APIRouter()

@router.get("/", response_model=List[DeviceResponse])
async def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implement list devices
    pass

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str, db: Session = Depends(get_db)):
    # TODO: Implement get device
    pass

@router.post("/", response_model=DeviceResponse)
async def register_device(device: DeviceCreate, db: Session = Depends(get_db)):
    # TODO: Implement register device
    pass
