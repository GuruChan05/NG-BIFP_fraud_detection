from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    device_type = Column(String)  # mobile, desktop, tablet
    os = Column(String)
    browser = Column(String)
    trust_score = Column(Float, default=0.5)
    is_trusted = Column(String, default="unknown")  # unknown, trusted, untrusted
    last_seen = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="devices")
