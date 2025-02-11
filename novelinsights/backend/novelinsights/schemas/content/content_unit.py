from uuid import UUID
from typing import Optional, List
from pydantic import Field

from novelinsights.schemas.base import BaseConfig, CoreBase
from novelinsights.schemas.knowledge.entity import EntityState


class ContentUnitBase(CoreBase):
    """Base schema for content unit without ID fields"""
    content: str
    content_token_count: Optional[int] = None
    entity_states: Optional[List[EntityState]] = Field(None, description="Associated entity states")
    context_id: Optional[UUID] = Field(None, description="Associated context ID")
    content_structure_id: Optional[UUID] = Field(None, description="Associated content structure ID")
    sequence: Optional[int] = Field(None, description="Position in the content structure")
    
# TODO: Add create schema

class ContentUnitCreate(ContentUnitBase):
    """Schema for creating a new content unit"""
    pass

class ContentUnit(ContentUnitBase):
    """Complete content unit schema with all fields"""
    ts_vector: Optional[str] = Field(None, description="Full text search vector")
    content_embedding: Optional[List[float]] = Field(None, description="Content embedding vector")
    
class ContentUnitUpdate(BaseConfig):
    """Schema for updating a content unit"""
    content: Optional[str] = None
    content_token_count: Optional[int] = None
    context_id: Optional[UUID] = Field(None, description="Updated context ID")
    content_structure_id: Optional[UUID] = Field(None, description="Updated content structure ID")
    sequence: Optional[int] = Field(None, description="Updated sequence position")

