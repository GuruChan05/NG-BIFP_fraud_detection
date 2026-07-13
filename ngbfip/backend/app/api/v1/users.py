from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    # TODO: Implement get current user
    pass

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implement get user
    pass

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: Implement create user
    pass
