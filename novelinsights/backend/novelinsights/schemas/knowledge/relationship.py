from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from novelinsights.models.knowledge.relationship import RelationDirectionType, RelationType, RelationStatusType
from novelinsights.schemas.base import CoreBase, TemporalSnapshotBase, BaseConfig



class NodeRelationshipStateBase(TemporalSnapshotBase):
    """Base schema for node relationship state without ID fields"""
    node_relationship_id: UUID
    status: RelationStatusType = RelationStatusType.ACTIVE
    strength: Optional[int] = Field(None, ge=1, le=5, description="1-5, 5 being the strongest connection")
    description: Optional[str] = None
    # properties are AI generated, with a flexible schema
    properties: Optional[Dict[str, Any]] = None
    agent_metadata_id: UUID
    

# TODO: Add create schema

class NodeRelationshipStateCreate(NodeRelationshipStateBase):
    """Schema for creating a new node relationship state"""
    pass

# TODO
class NodeRelationshipState(NodeRelationshipStateBase):
    """Complete node relationship state schema with all fields"""
    pass

class NodeRelationshipStateUpdate(BaseConfig):
    """Schema for updating a node relationship state"""
    status: Optional[RelationStatusType] = None
    strength: Optional[int] = Field(None, ge=1, le=5)
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    agent_metadata_id: Optional[UUID] = None
    parent_structure_id: Optional[UUID] = None
    current_structure_id: Optional[UUID] = None






class NodeRelationshipBase(CoreBase):
    """Base schema for node relationship without ID fields"""
    source_node_id: UUID
    target_node_id: UUID
    direction: RelationDirectionType
    relationship_type: RelationType
    current_status: RelationStatusType = RelationStatusType.ACTIVE
    subtype: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[NodeRelationshipState]] = None
    class Config:
        from_attributes = True

# TODO: Add create schema

class NodeRelationshipCreate(NodeRelationshipBase):
    """Schema for creating a new node relationship"""
    pass

# TODO

class NodeRelationship(NodeRelationshipBase):
    """Complete node relationship schema with all fields"""
    pass

class NodeRelationshipUpdate(BaseConfig):
    """Schema for updating a node relationship"""
    source_node_id: Optional[UUID] = None
    target_node_id: Optional[UUID] = None
    direction: Optional[RelationDirectionType] = None
    relationship_type: Optional[RelationType] = None
    current_status: Optional[RelationStatusType] = None
    subtype: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[NodeRelationshipState]] = None
