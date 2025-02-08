from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from novelinsights.models.knowledge.node import NodeType
from novelinsights.schemas.base import BaseConfig, CoreBase, TemporalSnapshotBase

class NodeStateBase(TemporalSnapshotBase):
    """Base schema for node state without ID fields"""
    node_id: UUID
    importance: Optional[int] = Field(None, ge=1, le=5, description="1-5, 1 being the most important")
    summary: Optional[str] = None # AI generated summary of the node
    knowledge: Optional[Dict[str, Any]] = None # flexible schema for AI generated knowledge about the node
    agent_metadata_id: UUID

# TODO

class NodeStateCreate(NodeStateBase):
    """Schema for creating a new node state"""
    pass

# TODO

class NodeState(NodeStateBase):
    """Complete node state schema with all fields"""
    pass

class NodeStateUpdate(BaseConfig):
    """Schema for updating a node state"""
    importance: Optional[int] = Field(None, ge=1, le=5)
    summary: Optional[str] = None # AI generated summary of the node
    knowledge: Optional[Dict[str, Any]] = None # flexible schema for AI generated knowledge about the node
    agent_metadata_id: Optional[UUID] = None
    parent_structure_id: Optional[UUID] = None
    current_structure_id: Optional[UUID] = None
        





class NodeBase(CoreBase):
    """Base schema for node without ID fields"""
    name: str
    node_type: NodeType
    optional_type: Optional[str] = None
    additional_types: Optional[List[str]] = None
        

# TODO: Add create schema

class NodeCreate(NodeBase):
    """Schema for creating a new node"""
    pass

# TODO

class Node(NodeBase):
    """Complete node schema with all fields"""
    pass

class NodeUpdate(BaseConfig):
    """Schema for updating a node"""
    name: Optional[str] = None
    node_type: Optional[NodeType] = None
    optional_type: Optional[str] = None
    additional_types: Optional[List[str]] = None
    states: Optional[List[NodeState]] = None
    
