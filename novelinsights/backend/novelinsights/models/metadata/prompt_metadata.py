# novelinsights/models/metadata.py

# SQLAlchemy core imports
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import (
    UUID,     # For UUID field type
    JSONB,    # For JSON fields with binary storage
)
from sqlalchemy.orm import relationship

from novelinsights.models.base import CoreBase
from novelinsights.types.services.prompt import PromptType

class PromptMetadata(CoreBase):
    __tablename__ = 'prompt_metadata'
    
    agent_metadata_id = Column(UUID(as_uuid=True), ForeignKey('agent_metadata.id'), nullable=False)
    agent_metadata = relationship('AgentMetadata', back_populates="prompt_metadata")
    
    model = Column(String(255), nullable=False) # The model used for the agent, e.g. "claude-3-opus-20240229"
    parameters = Column(JSONB)
    prompt_type = Column(SQLEnum(PromptType), nullable=False)
    prompt_version = Column(String(50), nullable=False) # 
    
    tokens_used = Column(Integer)
    