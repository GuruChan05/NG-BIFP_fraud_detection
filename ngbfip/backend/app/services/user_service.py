from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models.user import User
from app.db.models.login_history import LoginHistory
from app.core.security import get_password_hash, verify_password
from typing import Optional, List

class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def list_active_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, email: str, username: str, full_name: str, password: str) -> User:
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user_profile(db: Session, user_id: int, full_name: str = None, bio: str = None, 
                           phone_number: str = None, avatar_url: str = None, 
                           department: str = None) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        if full_name:
            user.full_name = full_name
        if bio is not None:
            user.bio = bio
        if phone_number:
            user.phone_number = phone_number
        if avatar_url:
            user.avatar_url = avatar_url
        if department:
            user.department = department
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if not verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.last_password_change = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def update_last_login(db: Session, user_id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def activate_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
    
    @staticmethod
    def add_login_history(db: Session, user_id: int, ip_address: str = None, 
                         user_agent: str = None, device_type: str = None) -> LoginHistory:
        login_record = LoginHistory(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type
        )
        db.add(login_record)
        db.commit()
        db.refresh(login_record)
        return login_record
    
    @staticmethod
    def get_user_login_history(db: Session, user_id: int, limit: int = 20) -> List[LoginHistory]:
        return db.query(LoginHistory).filter(LoginHistory.user_id == user_id).order_by(
            LoginHistory.login_time.desc()
        ).limit(limit).all()
