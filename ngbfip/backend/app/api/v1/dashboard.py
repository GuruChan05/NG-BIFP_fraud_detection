from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db

router = APIRouter()

@router.get("/overview")
async def dashboard_overview(db: Session = Depends(get_db)):
    # TODO: Implement dashboard overview
    return {"overview": "data"}

@router.get("/statistics")
async def dashboard_statistics(db: Session = Depends(get_db)):
    # TODO: Implement dashboard statistics
    return {"statistics": "data"}
