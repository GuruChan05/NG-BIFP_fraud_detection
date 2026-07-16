from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db)):
    from app.db.models.user import User
    # Default to first user as a mock for current user
    user = db.query(User).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    from app.db.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    from app.db.models.user import User
    from app.core.security import get_password_hash
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password) if hasattr(user, 'password') else "hashed"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
