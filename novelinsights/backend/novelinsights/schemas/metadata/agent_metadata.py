from typing import Optional, Dict, Any

from novelinsights.types import AgentType
from novelinsights.schemas.base import CoreBase, BaseConfig

class AgentMetadataBase(CoreBase):
    """Base schema for agent metadata without ID fields"""
    agent_type: AgentType
    agent_version: str
    tokens_used: Optional[int] = None
    success: bool
    error: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None

# TODO

class AgentMetadataCreate(AgentMetadataBase):
    """Schema for creating new agent metadata"""
    pass

# TODO

class AgentMetadata(AgentMetadataBase):
    """Complete agent metadata schema with all fields"""
    pass

class AgentMetadataUpdate(BaseConfig):
    """Schema for updating agent metadata"""
    agent_type: Optional[AgentType] = None
    agent_version: Optional[str] = None
    tokens_used: Optional[int] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None
