from uuid import UUID
from typing import Optional
from pydantic import EmailStr

from novelinsights.schemas.base import CoreBase, BaseConfig, SlugBase

class UserBase(CoreBase, SlugBase):
    """Base schema for user without ID fields"""
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None

# TODO

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str

class User(UserBase):
    """Complete user schema with all fields"""
    pass

# TODO

class UserUpdate(BaseConfig):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    