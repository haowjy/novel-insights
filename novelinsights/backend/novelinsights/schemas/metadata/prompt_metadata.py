from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel

from novelinsights.services.ai.prompts.types import PromptType
from novelinsights.schemas.base import CoreBase, BaseConfig

class PromptMetadataBase(CoreBase):
    """Base schema for prompt metadata without ID fields"""
    agent_metadata_id: UUID
    model: str
    parameters: Optional[Dict[str, Any]] = None
    prompt_type: PromptType
    prompt_version: str
    tokens_used: Optional[int] = None


# TODO

class PromptMetadataCreate(PromptMetadataBase):
    """Schema for creating new prompt metadata"""
    pass

# TODO

class PromptMetadata(PromptMetadataBase):
    """Complete prompt metadata schema with all fields"""
    pass

# TODO

class PromptMetadataUpdate(BaseConfig):
    """Schema for updating prompt metadata"""
    agent_metadata_id: Optional[UUID] = None
    model: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    prompt_type: Optional[PromptType] = None
    prompt_version: Optional[str] = None
    tokens_used: Optional[int] = None
