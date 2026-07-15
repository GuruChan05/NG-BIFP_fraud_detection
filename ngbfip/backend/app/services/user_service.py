"""User service for user management operations."""
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.user import User
from app.core.security import hash_password, verify_password
from app.core.audit import audit_logger
from app.core.logging import logger
from fastapi import HTTPException, status
from typing import Optional


class UserService:
    """Service for user management operations."""
    
    @staticmethod
    def create_user(
        db: Session,
        username: str,
        email: str,
        password: str,
        full_name: str,
        role: str = "user"
    ) -> User:
        """Create a new user.
        
        Args:
            db: Database session
            username: Username
            email: Email address
            password: Plain text password
            full_name: Full name
            role: User role
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If user already exists or database error
        """
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            logger.warning(f"Registration failed: User with email {email} already exists")
            audit_logger.log_action(
                user_id=None,
                action="REGISTER",
                resource_type="USER",
                resource_id=None,
                details={"email": email, "reason": "Duplicate email"},
                status="FAILURE"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        try:
            # Create new user
            user = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                hashed_password=hash_password(password),
                full_name=full_name,
                role=role,
                is_active=True
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User created successfully: {username}")
            audit_logger.log_action(
                user_id=user.id,
                action="REGISTER",
                resource_type="USER",
                resource_id=user.id,
                status="SUCCESS"
            )
            
            return user
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error during user creation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating user"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error during user creation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            )
    
    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user with email and password.
        
        Args:
            db: Database session
            email: Email address
            password: Plain text password
            
        Returns:
            User if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"Login failed: User with email {email} not found")
            audit_logger.log_login(email, False)
            return None
        
        if not user.is_active:
            logger.warning(f"Login failed: User {email} is inactive")
            audit_logger.log_login(email, False)
            return None
        
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Login failed: Invalid password for user {email}")
            audit_logger.log_login(email, False)
            return None
        
        logger.info(f"User authenticated successfully: {email}")
        audit_logger.log_login(email, True)
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email.
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: str,
        **kwargs
    ) -> Optional[User]:
        """Update user information.
        
        Args:
            db: Database session
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        try:
            for key, value in kwargs.items():
                if hasattr(user, key) and key not in ['id', 'hashed_password', 'created_at']:
                    setattr(user, key, value)
            
            db.commit()
            db.refresh(user)
            
            audit_logger.log_action(
                user_id=user_id,
                action="UPDATE",
                resource_type="USER",
                resource_id=user_id,
                details=kwargs
            )
            
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    @staticmethod
    def change_password(
        db: Session,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change user password.
        
        Args:
            db: Database session
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully
            
        Raises:
            HTTPException: If password change fails
        """
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_password(old_password, user.hashed_password):
            audit_logger.log_action(
                user_id=user_id,
                action="CHANGE_PASSWORD",
                resource_type="USER",
                resource_id=user_id,
                status="FAILURE"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        try:
            user.hashed_password = hash_password(new_password)
            db.commit()
            
            audit_logger.log_action(
                user_id=user_id,
                action="CHANGE_PASSWORD",
                resource_type="USER",
                resource_id=user_id,
                status="SUCCESS"
            )
            
            logger.info(f"Password changed successfully for user: {user_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error changing password: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error changing password"
            )


user_service = UserService()
