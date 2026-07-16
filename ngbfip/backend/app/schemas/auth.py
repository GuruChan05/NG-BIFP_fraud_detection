from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str    
