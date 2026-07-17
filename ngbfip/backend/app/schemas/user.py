from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    department: Optional[str] = None

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_verified: bool
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    is_admin: bool
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class LoginHistoryResponse(BaseModel):
    id: int
    login_time: datetime
    logout_time: Optional[datetime]
    ip_address: Optional[str]
    device_type: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True
