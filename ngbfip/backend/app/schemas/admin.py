"""Admin schemas for API responses."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RoleResponse(BaseModel):
    """Response schema for roles."""
    id: int
    name: str
    description: Optional[str]
    is_system: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    """Response schema for permissions."""
    id: int
    name: str
    description: Optional[str]
    resource: str
    action: str
    created_at: datetime

    class Config:
        from_attributes = True


class RoleDetailResponse(RoleResponse):
    """Detailed role response with permissions."""
    permissions: List[PermissionResponse] = []


class UserAdminResponse(BaseModel):
    """Response schema for user in admin context."""
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    is_admin: bool
    is_verified: bool
    phone_number: Optional[str]
    department: Optional[str]
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStatsResponse(BaseModel):
    """Response schema for admin dashboard statistics."""
    total_users: int
    active_users: int
    inactive_users: int
    admin_users: int
    total_roles: int
    total_permissions: int
    recent_audit_logs: int


class AuditLogResponse(BaseModel):
    """Response schema for audit logs."""
    id: int
    user_id: int
    action: str
    entity: str
    entity_id: int
    changes: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SystemLogResponse(BaseModel):
    """Response schema for system logs."""
    id: int
    log_level: str
    service: str
    message: str
    error_details: Optional[str]
    status_code: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class RoleCreateRequest(BaseModel):
    """Request schema for creating a role."""
    name: str
    description: Optional[str] = None


class PermissionCreateRequest(BaseModel):
    """Request schema for creating a permission."""
    name: str
    resource: str
    action: str
    description: Optional[str] = None


class AssignRoleRequest(BaseModel):
    """Request schema for assigning role to user."""
    role_id: int


class AssignPermissionRequest(BaseModel):
    """Request schema for assigning permission to role."""
    permission_id: int
