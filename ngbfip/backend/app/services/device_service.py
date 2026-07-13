from sqlalchemy.orm import Session
from app.db.models.device import Device

class DeviceService:
    @staticmethod
    def get_device_by_id(db: Session, device_id: str):
        return db.query(Device).filter(Device.device_id == device_id).first()

    @staticmethod
    def list_devices(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
        query = db.query(Device)
        if user_id:
            query = query.filter(Device.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def register_device(db: Session, device_data: dict):
        device = Device(**device_data)
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
