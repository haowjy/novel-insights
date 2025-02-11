from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from novelinsights.models.knowledge.entity import EntityType
from novelinsights.schemas.base import BaseConfig, CoreBase, TemporalSnapshotBase

class EntityStateBase(TemporalSnapshotBase):
    """Base schema for entity state without ID fields"""
    entity_id: UUID
    importance: Optional[int] = Field(None, ge=1, le=5, description="1-5, 1 being the most important")
    summary: Optional[str] = None # AI generated summary of the entity
    knowledge: Optional[Dict[str, Any]] = None # flexible schema for AI generated knowledge about the entity
    agent_metadata_id: UUID

# TODO

class EntityStateCreate(EntityStateBase):
    """Schema for creating a new entity state"""
    pass

# TODO

class EntityState(EntityStateBase):
    """Complete entity state schema with all fields"""
    pass

class EntityStateUpdate(BaseConfig):
    """Schema for updating an entity state"""
    importance: Optional[int] = Field(None, ge=1, le=5)
    summary: Optional[str] = None # AI generated summary of the entity
    knowledge: Optional[Dict[str, Any]] = None # flexible schema for AI generated knowledge about the entity
    agent_metadata_id: Optional[UUID] = None
    parent_structure_id: Optional[UUID] = None
    current_structure_id: Optional[UUID] = None
        





class EntityBase(CoreBase):
    """Base schema for entity without ID fields"""
    name: str
    entity_type: EntityType
    optional_type: Optional[str] = None
    additional_types: Optional[List[str]] = None
        

# TODO: Add create schema

class EntityCreate(EntityBase):
    """Schema for creating a new entity"""
    pass

# TODO

class Entity(EntityBase):
    """Complete entity schema with all fields"""
    pass

class EntityUpdate(BaseConfig):
    """Schema for updating an entity"""
    name: Optional[str] = None
    entity_type: Optional[EntityType] = None
    optional_type: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[EntityState]] = None
    
