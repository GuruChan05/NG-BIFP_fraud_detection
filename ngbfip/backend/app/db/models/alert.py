from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    alert_type = Column(String)  # suspicious_activity, high_risk, etc.
    severity = Column(String)  # low, medium, high, critical
    description = Column(String)
    is_resolved = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="alerts")
    transaction = relationship("Transaction", back_populates="alerts")
