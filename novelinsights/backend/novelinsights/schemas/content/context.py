from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum

from novelinsights.models.content.context import ContextScope, ContextType

from novelinsights.schemas.base import BaseConfig, CoreBase, SlugBase
from novelinsights.schemas.content.content_unit import ContentUnit
from novelinsights.schemas.content.structure import ContentStructure
from novelinsights.schemas.knowledge.node import NodeState

class ContextBase(CoreBase, SlugBase): # NOTE: Do we need to inherit from SlugBase?
    """Base schema for context without ID fields"""
    type: ContextType = Field(..., description="Type of context")
    scope: ContextScope = Field(..., description="Scope of context")
    title: str = Field(..., max_length=255, description="Title of the context")
    content: str = Field(..., description="Content of the context")
    properties: Optional[Dict[str, Any]] = Field(None, description="Additional properties")
    sequence: Optional[int] = Field(None, description="Ordering within same type/scope")

# TODO: Add create schema

class ContextCreate(ContextBase):
    """Schema for creating a new context"""
    pass

# TODO

class Context(ContextBase):
    """Complete context schema with all fields"""
    structures: List[ContentStructure] = Field([], description="Associated content structures")
    content_units: List[ContentUnit] = Field([], description="Associated content units")
    node_states: List[NodeState] = Field([], description="Associated node states")

class ContextUpdate(BaseConfig):
    """Schema for updating a context"""
    type: Optional[ContextType] = Field(None, description="Updated type of context")
    scope: Optional[ContextScope] = Field(None, description="Updated scope of context")
    title: Optional[str] = Field(None, max_length=255, description="Updated title")
    content: Optional[str] = Field(None, description="Updated content")
    properties: Optional[Dict[str, Any]] = Field(None, description="Updated properties")
    sequence: Optional[int] = Field(None, description="Updated sequence")