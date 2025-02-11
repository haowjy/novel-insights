from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from novelinsights.models.knowledge.relationship import RelationDirectionType, RelationType, RelationStatusType
from novelinsights.schemas.base import CoreBase, TemporalSnapshotBase, BaseConfig



class RelationshipStateBase(TemporalSnapshotBase):
    """Base schema for relationship states"""
    relationship_id: UUID
    status: RelationStatusType = RelationStatusType.ACTIVE
    strength: Optional[int] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    agent_metadata_id: UUID


class RelationshipStateCreate(RelationshipStateBase):
    """Schema for creating a new relationship state"""
    pass


class RelationshipState(RelationshipStateBase):
    """Schema for a relationship state with all fields"""
    id: UUID


class RelationshipStateUpdate(BaseConfig):
    """Schema for updating a relationship state"""
    status: Optional[RelationStatusType] = None
    strength: Optional[int] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    agent_metadata_id: Optional[UUID] = None


class RelationshipBase(CoreBase):
    """Base schema for relationships"""
    source_entity_id: UUID
    target_entity_id: UUID
    direction: RelationDirectionType
    relationship_type: RelationType
    subtype: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[RelationshipState]] = None


class RelationshipCreate(RelationshipBase):
    """Schema for creating a new relationship"""
    pass


class Relationship(RelationshipBase):
    """Schema for a relationship with all fields"""
    id: UUID


class RelationshipUpdate(BaseConfig):
    """Schema for updating a relationship"""
    source_entity_id: Optional[UUID] = None
    target_entity_id: Optional[UUID] = None
    direction: Optional[RelationDirectionType] = None
    relationship_type: Optional[RelationType] = None
    subtype: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[RelationshipState]] = None
