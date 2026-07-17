"""Admin API endpoints for user, role, and permission management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models.user import User
from app.schemas.admin import (
    RoleResponse, PermissionResponse, RoleDetailResponse, UserAdminResponse,
    DashboardStatsResponse, AuditLogResponse, SystemLogResponse,
    RoleCreateRequest, PermissionCreateRequest, AssignRoleRequest, AssignPermissionRequest
)
from app.services.admin_service import AdminService
from app.api.deps import get_current_active_user, get_current_admin_user
from typing import List

router = APIRouter()


# Admin Dashboard
@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_admin_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get admin dashboard statistics."""
    return AdminService.get_dashboard_stats(db)


# User Management
@router.get("/users", response_model=List[UserAdminResponse])
async def list_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all users with pagination (admin only)."""
    users, total = AdminService.get_all_users(db, skip, limit)
    return users


@router.get("/users/search")
async def search_users(
    q: str,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Search users by email, username, or full_name (admin only)."""
    return AdminService.search_users(db, q, limit)


@router.get("/users/{user_id}", response_model=UserAdminResponse)
async def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get user details (admin only)."""
    user = AdminService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/activate")
async def activate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Activate a user (admin only)."""
    user = AdminService.activate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User activated successfully", "user": UserAdminResponse.from_orm(user)}


@router.post("/users/{user_id}/deactivate")
async def deactivate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Deactivate a user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    user = AdminService.deactivate_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deactivated successfully"}


@router.delete("/users/{user_id}")
async def delete_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    success = AdminService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.post("/users/{user_id}/promote")
async def promote_user_to_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Promote user to admin (admin only)."""
    user = AdminService.promote_to_admin(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User promoted to admin"}


@router.post("/users/{user_id}/demote")
async def demote_user_from_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Demote admin user to regular user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot demote yourself")
    
    user = AdminService.demote_from_admin(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User demoted from admin"}


# Role Management
@router.get("/roles", response_model=List[RoleResponse])
async def list_all_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all roles (admin only)."""
    return AdminService.get_all_roles(db)


@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new role (admin only)."""
    role = AdminService.create_role(db, role_data.name, role_data.description)
    return role


@router.get("/roles/{role_id}", response_model=RoleDetailResponse)
async def get_role_details(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get role details including permissions (admin only)."""
    role = AdminService.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/roles/{role_id}")
async def update_role(
    role_id: int,
    role_data: RoleCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update role (admin only)."""
    role = AdminService.update_role(db, role_id, role_data.name, role_data.description)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role updated successfully", "role": role}


@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a role (admin only, cannot delete system roles)."""
    success = AdminService.delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found or is a system role")
    return {"message": "Role deleted successfully"}


# Permission Management
@router.get("/permissions", response_model=List[PermissionResponse])
async def list_all_permissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all permissions (admin only)."""
    return AdminService.get_all_permissions(db)


@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_data: PermissionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new permission (admin only)."""
    permission = AdminService.create_permission(
        db, 
        permission_data.name,
        permission_data.resource,
        permission_data.action,
        permission_data.description
    )
    return permission


# Role-Permission Assignment
@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Assign a permission to a role (admin only)."""
    role = AdminService.assign_permission_to_role(db, role_id, permission_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role or permission not found")
    return {"message": "Permission assigned to role successfully"}


@router.delete("/roles/{role_id}/permissions/{permission_id}")
async def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Remove a permission from a role (admin only)."""
    role = AdminService.remove_permission_from_role(db, role_id, permission_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role or permission not found")
    return {"message": "Permission removed from role successfully"}


# User-Role Assignment
@router.post("/users/{user_id}/roles/{role_id}")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Assign a role to a user (admin only)."""
    user = AdminService.assign_role_to_user(db, user_id, role_id)
    if not user:
        raise HTTPException(status_code=404, detail="User or role not found")
    return {"message": "Role assigned to user successfully"}


@router.delete("/users/{user_id}/roles/{role_id}")
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Remove a role from a user (admin only)."""
    user = AdminService.remove_role_from_user(db, user_id, role_id)
    if not user:
        raise HTTPException(status_code=404, detail="User or role not found")
    return {"message": "Role removed from user successfully"}


# Audit Logs
@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get audit logs (admin only)."""
    logs, total = AdminService.get_audit_logs(db, skip, limit)
    return logs


@router.get("/audit-logs/user/{user_id}")
async def get_user_audit_logs(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get audit logs for a specific user (admin only)."""
    logs = AdminService.get_audit_logs_by_user(db, user_id, skip, limit)
    return logs


# System Logs
@router.get("/system-logs", response_model=List[SystemLogResponse])
async def get_system_logs(
    skip: int = 0,
    limit: int = 50,
    level: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get system logs with optional level filter (admin only)."""
    logs, total = AdminService.get_system_logs(db, skip, limit, level)
    return logs
