"""Fraud prediction database model."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class FraudPrediction(Base):
    """Model for storing fraud predictions."""
    __tablename__ = "fraud_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    risk_score = Column(Float, default=0.0)  # 0.0 to 1.0
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    is_fraudulent = Column(String, default="unknown")  # legitimate, fraudulent, suspicious
    risk_level = Column(String, default="low")  # low, medium, high, critical
    explanation = Column(Text)  # Explanation of the prediction
    contributing_factors = Column(Text)  # JSON-encoded list of factors
    recommendations = Column(Text)  # JSON-encoded list of recommendations
    model_name = Column(String, default="default_fraud_detection")
    model_version = Column(String, default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User")
    transaction = relationship("Transaction")
