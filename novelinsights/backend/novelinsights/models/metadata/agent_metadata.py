# novelinsights/models/metadata/agent_metadata.py

# SQLAlchemy core imports
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Text,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import (
    JSONB,    # For JSON fields with binary storage
)
from sqlalchemy.orm import relationship

from novelinsights.models.base import CoreBase
from novelinsights.services.ai.agents.types import AgentType

class AgentMetadata(CoreBase):
    __tablename__ = 'agent_metadata'
    
    # # Polymorphic parent relationship
    # parent_id = Column(UUID(as_uuid=True), nullable=False)
    # parent_type = Column(String(50), nullable=False)
    
    # Agent info
    agent_type = Column(SQLEnum(AgentType), nullable=False)
    agent_version = Column(String(50), nullable=False)
    
    # Execution info
    tokens_used = Column(Integer) # The number of tokens used in the agent's execution
    success = Column(Boolean, nullable=False) # Whether the agent's execution was successful
    error = Column(Text) # The error that occurred in the agent's execution
    
    # Prompt metadata history
    prompt_metadata = relationship('PromptMetadata', back_populates="agent_metadata")
    
    # Optional metadata that might change
    extra_metadata = Column('metadata', JSONB)  # Additional metadata about the agent's execution