from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel

from novelinsights.models.content.structure import ContentStructureType
from novelinsights.schemas.base import BaseConfig, CoreBase, SlugBase

class ContentStructureBase(CoreBase, SlugBase): # NOTE: Do we need to inherit from SlugBase?
    """Base schema for content structure without ID fields"""
    type: ContentStructureType
    title: str
    parent_id: Optional[UUID] = None
    sequence: Optional[int] = None
    meta_info: Optional[Dict[str, Any]] = None
    ai_summary: Optional[str] = None
    is_published: bool = False
    is_canonical: bool = False
    is_supplementary: bool = False

# TODO: Add create schema

class ContentStructureCreate(ContentStructureBase):
    """Schema for creating a new content structure"""
    pass

class ContentStructure(ContentStructureBase):
    """Complete content structure schema with all fields"""
    pass

class ContentStructureUpdate(BaseConfig):
    """Schema for updating a content structure"""
    type: Optional[ContentStructureType] = None
    title: Optional[str] = None
    parent_id: Optional[UUID] = None
    sequence: Optional[int] = None
    meta_info: Optional[Dict[str, Any]] = None
    ai_summary: Optional[str] = None
    is_published: Optional[bool] = None
    is_canonical: Optional[bool] = None
    is_supplementary: Optional[bool] = None
