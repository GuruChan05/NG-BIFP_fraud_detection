"""Report database model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Report(Base):
    """Model for storing generated reports."""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_type = Column(String, index=True)  # fraud, transaction, user, audit
    title = Column(String)
    description = Column(Text, nullable=True)
    
    # Date range filters
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    
    # Report data
    total_records = Column(Integer, default=0)
    total_amount = Column(Float, default=0.0)
    fraud_count = Column(Integer, default=0)
    fraud_percentage = Column(Float, default=0.0)
    
    # Export format
    export_format = Column(String, default="pdf")  # pdf, csv, xlsx
    file_path = Column(String, nullable=True)
    file_size = Column(Integer, default=0)
    
    # Status and metadata
    status = Column(String, default="pending")  # pending, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")
