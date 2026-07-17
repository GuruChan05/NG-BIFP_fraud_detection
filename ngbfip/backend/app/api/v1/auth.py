from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.base import get_db
from app.schemas.auth import (
    TokenRequest, TokenResponse, UserRegister, TokenRefresh, ChangePasswordRequest
)
from app.core.security import (
    verify_password, create_access_token, create_refresh_token, 
    validate_password, get_password_hash, decode_token
)
from app.db.models.user import User
from app.services.user_service import UserService
from app.api.deps import get_current_user, get_current_active_user

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegister, 
    db: Session = Depends(get_db),
    user_agent: str = Header(None)
):
    """Register a new user account."""
    
    # Validate passwords match
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )
    
    # Check email uniqueness
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check username uniqueness
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Validate password strength
    if not validate_password(user_data.password):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a digit."
        )
    
    # Create new user
    new_user = UserService.create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        password=user_data.password
    )
    
    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: TokenRequest, 
    db: Session = Depends(get_db),
    user_agent: str = Header(None)
):
    """Authenticate user and return JWT tokens."""
    
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    # Update last login
    UserService.update_last_login(db, user.id)
    
    # Add login history
    UserService.add_login_history(
        db=db,
        user_id=user.id,
        user_agent=user_agent,
        device_type="web"
    )
    
    # Generate tokens
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_data: TokenRefresh):
    """Refresh access token using refresh token."""
    
    payload = decode_token(refresh_data.refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    email = payload.get("sub")
    user_id = payload.get("user_id")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )
    
    # Generate new tokens
    access_token = create_access_token(data={"sub": email, "user_id": user_id})
    refresh_token = create_refresh_token(data={"sub": email, "user_id": user_id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (client-side token cleanup)."""
    return {"message": "Logged out successfully"}

@router.post("/change-password")
async def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Change user password."""
    
    # Verify old password
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    # Check new password is different
    if password_data.old_password == password_data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )
    
    # Update password
    success = UserService.change_password(
        db=db,
        user_id=current_user.id,
        old_password=password_data.old_password,
        new_password=password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to change password"
        )
    
    return {"message": "Password changed successfully"}
