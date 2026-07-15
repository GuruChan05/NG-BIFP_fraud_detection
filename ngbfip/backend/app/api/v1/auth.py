"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas.auth import TokenRequest, TokenResponse, UserRegister, PasswordReset, PasswordResetConfirm
from app.schemas.user import UserResponse
from app.core.security import create_access_token, create_refresh_token, get_current_user
from app.core.config import settings
from app.core.logging import logger
from app.services.user_service import user_service
from app.core.audit import audit_logger
from typing import Dict, Any

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user information
    """
    try:
        user = user_service.create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            role="user"
        )
        
        logger.info(f"User registered successfully: {user.email}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: TokenRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token.
    
    Args:
        credentials: Login credentials
        db: Database session
        
    Returns:
        JWT tokens and user info
    """
    try:
        user = user_service.authenticate_user(
            db=db,
            email=credentials.email,
            password=credentials.password
        )
        
        if not user:
            logger.warning(f"Login failed for email: {credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": user.id, "email": user.email}
        )
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (client should discard token).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Logout confirmation
    """
    logger.info(f"User logged out: {current_user.get('email')}")
    audit_logger.log_action(
        user_id=current_user.get('sub'),
        action="LOGOUT",
        resource_type="USER",
        resource_id=current_user.get('sub')
    )
    return {"message": "Logged out successfully"}


@router.post("/forgot-password")
async def forgot_password(data: PasswordReset, db: Session = Depends(get_db)):
    """Request password reset (sends email).
    
    Args:
        data: Email for password reset
        db: Database session
        
    Returns:
        Confirmation message
    """
    user = user_service.get_user_by_email(db, data.email)
    
    if user:
        logger.info(f"Password reset requested for: {data.email}")
        audit_logger.log_action(
            user_id=user.id,
            action="FORGOT_PASSWORD",
            resource_type="USER",
            resource_id=user.id
        )
        # TODO: Send password reset email
    
    # Always return success to prevent user enumeration
    return {"message": "If the email exists, a password reset link will be sent"}


@router.post("/reset-password")
async def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password with token.
    
    Args:
        data: Reset token and new password
        db: Database session
        
    Returns:
        Confirmation message
    """
    # TODO: Verify reset token and get user
    # For now, this is a placeholder
    return {"message": "Password reset successful"}


@router.post("/refresh")
async def refresh_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Refresh access token using refresh token.
    
    Args:
        current_user: Current user from refresh token
        
    Returns:
        New access token
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": current_user.get('sub'), "email": current_user.get('email')},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
