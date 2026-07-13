from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.auth import TokenRequest, TokenResponse
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(credentials: TokenRequest, db: Session = Depends(get_db)):
    # TODO: Implement login logic
    return {"access_token": "token", "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
