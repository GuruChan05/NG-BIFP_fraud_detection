"""System Log database model."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base


class SystemLog(Base):
    """Model for storing system-level logs."""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_level = Column(String(20), default="INFO")  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    service = Column(String(100))  # service name
    message = Column(Text)
    error_details = Column(Text, nullable=True)
    status_code = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
