from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash
from app.db.models.user import User

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_user(db: Session, email: str, username: str, full_name: str, password: str):
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
