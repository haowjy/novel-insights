from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

from novelinsights.models.content.context import ContextScope, ContextType

from novelinsights.schemas.base import BaseConfig, CoreBase, SlugBase
from novelinsights.schemas.content.content_unit import ContentUnit
from novelinsights.schemas.content.structure import ContentStructure
from novelinsights.schemas.knowledge.entity import EntityState

class ContextBase(CoreBase, SlugBase): # NOTE: Do we need to inherit from SlugBase?
    """Base schema for context without ID fields"""
    name: str
    description: Optional[str] = None
    type: ContextType
    scope: ContextScope
    parent_id: Optional[UUID] = None
    content_structure_id: Optional[UUID] = None
    entity_states: List[EntityState] = Field([], description="Associated entity states")

# TODO: Add create schema

class ContextCreate(ContextBase):
    """Schema for creating a new context"""
    pass

# TODO

class Context(ContextBase):
    """Complete context schema with all fields"""
    structures: List[ContentStructure] = Field([], description="Associated content structures")
    content_units: List[ContentUnit] = Field([], description="Associated content units")

class ContextUpdate(BaseConfig):
    """Schema for updating a context"""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ContextType] = None
    scope: Optional[ContextScope] = None
    parent_id: Optional[UUID] = None
    content_structure_id: Optional[UUID] = None