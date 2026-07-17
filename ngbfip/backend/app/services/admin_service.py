"""Admin service for managing users, roles, and permissions."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.audit_log import AuditLog
from app.db.models.system_log import SystemLog
from app.core.security import get_password_hash
from typing import List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AdminService:
    """Service for admin operations."""

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 50) -> Tuple[List[User], int]:
        """Get all users with pagination."""
        total = db.query(func.count(User.id)).scalar() or 0
        users = db.query(User).offset(skip).limit(limit).all()
        return users, total

    @staticmethod
    def search_users(db: Session, query: str, limit: int = 20) -> List[User]:
        """Search users by email, username, or full_name."""
        return db.query(User).filter(
            (User.email.ilike(f"%{query}%")) |
            (User.username.ilike(f"%{query}%")) |
            (User.full_name.ilike(f"%{query}%"))
        ).limit(limit).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def activate_user(db: Session, user_id: int) -> Optional[User]:
        """Activate a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.is_active = True
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} activated")
        return user

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> Optional[User]:
        """Deactivate a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.is_active = False
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} deactivated")
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user and all related data."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        logger.info(f"User {user_id} deleted")
        return True

    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
        """Update user information."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                if key == "hashed_password":
                    setattr(user, key, get_password_hash(value))
                else:
                    setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} updated")
        return user

    @staticmethod
    def promote_to_admin(db: Session, user_id: int) -> Optional[User]:
        """Promote user to admin."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.is_admin = True
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} promoted to admin")
        return user

    @staticmethod
    def demote_from_admin(db: Session, user_id: int) -> Optional[User]:
        """Demote admin user to regular user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.is_admin = False
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id} demoted from admin")
        return user

    # Role management
    @staticmethod
    def create_role(db: Session, name: str, description: str = None) -> Role:
        """Create a new role."""
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
        logger.info(f"Role {name} created")
        return role

    @staticmethod
    def get_all_roles(db: Session) -> List[Role]:
        """Get all roles."""
        return db.query(Role).all()

    @staticmethod
    def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
        """Get role by ID."""
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def update_role(db: Session, role_id: int, name: str = None, description: str = None) -> Optional[Role]:
        """Update role information."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        if name:
            role.name = name
        if description:
            role.description = description
        db.commit()
        db.refresh(role)
        logger.info(f"Role {role_id} updated")
        return role

    @staticmethod
    def delete_role(db: Session, role_id: int) -> bool:
        """Delete a role if not a system role."""
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role or role.is_system:
            return False
        db.delete(role)
        db.commit()
        logger.info(f"Role {role_id} deleted")
        return True

    @staticmethod
    def assign_role_to_user(db: Session, user_id: int, role_id: int) -> Optional[User]:
        """Assign a role to a user."""
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.id == role_id).first()
        if not user or not role:
            return None
        
        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            db.refresh(user)
            logger.info(f"Role {role_id} assigned to user {user_id}")
        
        return user

    @staticmethod
    def remove_role_from_user(db: Session, user_id: int, role_id: int) -> Optional[User]:
        """Remove a role from a user."""
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.id == role_id).first()
        if not user or not role:
            return None
        
        if role in user.roles:
            user.roles.remove(role)
            db.commit()
            db.refresh(user)
            logger.info(f"Role {role_id} removed from user {user_id}")
        
        return user

    # Permission management
    @staticmethod
    def create_permission(db: Session, name: str, resource: str, action: str, description: str = None) -> Permission:
        """Create a new permission."""
        permission = Permission(name=name, resource=resource, action=action, description=description)
        db.add(permission)
        db.commit()
        db.refresh(permission)
        logger.info(f"Permission {name} created")
        return permission

    @staticmethod
    def get_all_permissions(db: Session) -> List[Permission]:
        """Get all permissions."""
        return db.query(Permission).all()

    @staticmethod
    def get_permission_by_id(db: Session, permission_id: int) -> Optional[Permission]:
        """Get permission by ID."""
        return db.query(Permission).filter(Permission.id == permission_id).first()

    @staticmethod
    def assign_permission_to_role(db: Session, role_id: int, permission_id: int) -> Optional[Role]:
        """Assign a permission to a role."""
        role = db.query(Role).filter(Role.id == role_id).first()
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not role or not permission:
            return None
        
        if permission not in role.permissions:
            role.permissions.append(permission)
            db.commit()
            db.refresh(role)
            logger.info(f"Permission {permission_id} assigned to role {role_id}")
        
        return role

    @staticmethod
    def remove_permission_from_role(db: Session, role_id: int, permission_id: int) -> Optional[Role]:
        """Remove a permission from a role."""
        role = db.query(Role).filter(Role.id == role_id).first()
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not role or not permission:
            return None
        
        if permission in role.permissions:
            role.permissions.remove(permission)
            db.commit()
            db.refresh(role)
            logger.info(f"Permission {permission_id} removed from role {role_id}")
        
        return role

    # Audit logs
    @staticmethod
    def get_audit_logs(db: Session, skip: int = 0, limit: int = 50) -> Tuple[List[AuditLog], int]:
        """Get audit logs with pagination."""
        total = db.query(func.count(AuditLog.id)).scalar() or 0
        logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
        return logs, total

    @staticmethod
    def get_audit_logs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[AuditLog]:
        """Get audit logs for a specific user."""
        return db.query(AuditLog).filter(AuditLog.user_id == user_id).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

    # System logs
    @staticmethod
    def get_system_logs(db: Session, skip: int = 0, limit: int = 50, level: str = None) -> Tuple[List[SystemLog], int]:
        """Get system logs with pagination."""
        query = db.query(SystemLog)
        if level:
            query = query.filter(SystemLog.log_level == level)
        
        total = query.count()
        logs = query.order_by(SystemLog.created_at.desc()).offset(skip).limit(limit).all()
        return logs, total

    @staticmethod
    def log_system_event(db: Session, log_level: str, service: str, message: str, error_details: str = None, status_code: int = None) -> SystemLog:
        """Log a system event."""
        log = SystemLog(
            log_level=log_level,
            service=service,
            message=message,
            error_details=error_details,
            status_code=status_code
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_dashboard_stats(db: Session) -> dict:
        """Get dashboard statistics."""
        total_users = db.query(func.count(User.id)).scalar() or 0
        active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
        admin_users = db.query(func.count(User.id)).filter(User.is_admin == True).scalar() or 0
        
        total_roles = db.query(func.count(Role.id)).scalar() or 0
        total_permissions = db.query(func.count(Permission.id)).scalar() or 0
        
        recent_audit_logs = db.query(func.count(AuditLog.id)).scalar() or 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "admin_users": admin_users,
            "total_roles": total_roles,
            "total_permissions": total_permissions,
            "recent_audit_logs": recent_audit_logs
        }
