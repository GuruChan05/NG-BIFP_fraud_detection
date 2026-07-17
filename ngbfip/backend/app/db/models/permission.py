"""Permission database model."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base


class Permission(Base):
    """Model for storing permissions."""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    resource = Column(String(100))  # users, transactions, reports, admin
    action = Column(String(50))  # create, read, update, delete
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Note: Relationships are defined in role.py via secondary table
