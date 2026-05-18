from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    VOLUNTARIO = "voluntario"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.VOLUNTARIO
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8) # senha só existe na criação

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True