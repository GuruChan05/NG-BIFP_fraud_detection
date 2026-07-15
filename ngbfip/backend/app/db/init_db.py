from sqlalchemy import inspect
from app.db.session import engine
from app.db.models import (
    User,
    Transaction,
    Alert,
    Device,
    Notification,
    AuditLog,
)
from app.core.logging import logger


def init_db():
    """Initialize database tables."""
    try:
        # Create all tables
        from app.db.session import Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Print table information
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables created: {', '.join(tables)}")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


if __name__ == "__main__":
    init_db()
