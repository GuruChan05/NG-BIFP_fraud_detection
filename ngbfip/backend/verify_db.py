import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import inspect
from app.db.base import engine

def verify():
    try:
        # Try to connect and inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print("✅ Successfully connected to the database!")
        print("Existing tables in the database:")
        for table in tables:
            print(f" - {table}")
            
        required_tables = ["users", "transactions", "alerts", "devices", "notifications", "audit_logs"]
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"\n⚠️ The following required tables are missing: {', '.join(missing)}")
            print("Please make sure you have run the Alembic migrations: alembic upgrade head")
        elif not tables:
            print("\n⚠️ No tables found. Please run the Alembic migrations: alembic upgrade head")
        else:
            print("\n✅ All required tables are present.")
            
    except Exception as e:
        print("❌ Failed to connect to the database. Error details:")
        print(str(e))
        print("\nPlease ensure PostgreSQL is running and credentials in .env are correct.")

if __name__ == "__main__":
    verify()
