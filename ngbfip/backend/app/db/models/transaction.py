from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    transaction_type = Column(String)  # debit, credit, transfer
    merchant = Column(String, index=True)
    merchant_category = Column(String)
    location = Column(String)
    device_id = Column(String)
    risk_score = Column(Float, default=0.0)
    is_fraudulent = Column(String, default="unknown", index=True)  # unknown, legitimate, fraudulent
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="transactions")
    alerts = relationship("Alert", back_populates="transaction")
