# novelinsights/models/knowledge/relationship.py

# SQLAlchemy core imports
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Text,
    Enum as SQLEnum,
    Table  # <-- Import Table so we can build association tables
)
from sqlalchemy.dialects.postgresql import (
    UUID,     # For UUID field type
    JSONB,    # For JSON fields with binary storage
    ARRAY     # For array fields
)
from sqlalchemy.orm import relationship

from novelinsights.models.base import Base, TemporalSnapshotMixin, CoreBase
from novelinsights.types.core import CreationSourceType
from novelinsights.types.knowledge import RelationDirectionType, RelationStatusType, RelationType

"""

This file contains the SQLAlchemy models for representing relationships in the knowledge graph.

Key components:
- Association tables for many-to-many relationships between relationships and contexts/content units
- Enums defining relationship directions, types, and statuses
- Models for relationship states and relationships themselves

The models are used to represent connections between entities in the knowledge graph, capturing:
- Directionality (outbound, inbound, bidirectional)
- Type (family, friendship, rivalry, etc.)
- Status (active, dormant)
- Temporal snapshots of relationship states
- Associations with content units and contexts

These models form the core of the relationship representation in the knowledge graph system.

"""

# NEW: Define the association table for Relationship <--> Context
relationship_context = Table(
    "relationship_context",
    Base.metadata,
    Column('relationship_id', UUID(as_uuid=True), ForeignKey("relationship.id"), primary_key=True),
    Column('context_id', UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True),
    Column('source', SQLEnum(CreationSourceType))
)

# NEW: Define the association table for Relationship <--> ContentUnit
relationship_contentunit = Table(   
    "relationship_contentunit",
    Base.metadata,
    Column('relationship_id', UUID(as_uuid=True), ForeignKey("relationship.id"), primary_key=True),
    Column('content_unit_id', UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
    Column('source', SQLEnum(CreationSourceType))
)

class RelationshipState(TemporalSnapshotMixin, CoreBase):
    """
    A relationship state represents the state of a relationship at a specific point
    in the content or context.
    """
    __tablename__ = 'relationship_state'
    
    # Override creation source for relationship_states to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                         nullable=False, 
                         default=CreationSourceType.AI,
                         index=True)
    
    relationship_id = Column(UUID(as_uuid=True), ForeignKey('relationship.id'), nullable=False)
    parent_relationship = relationship('Relationship', back_populates='states')

    # Status at this point in content
    status = Column(SQLEnum(RelationStatusType), 
                   nullable=False, 
                   default=RelationStatusType.ACTIVE)
    
    # AI-generated fields
    strength = Column(Integer, comment="1-5, 5 being the strongest connection")
    description = Column(Text)  # Brief description of the relationship state
    
     # If we need structured data about the relationship, keep it focused on the connection
    properties = Column(JSONB,
        comment="""
        Flexible schema for AI generated relationship properties
        
        Example:
        {
            "status": str,      # e.g., "active", "strained", "broken"
            "dynamics": str,    # e.g., "supportive", "antagonistic"
            "evidence": list    # References to supporting content
        }
        """
    )
    
    # Agent metadata if this state was created by an AI agent
    agent_metadata_id = Column(UUID(as_uuid=True), ForeignKey('agent_metadata.id'), nullable=False)
    agent_metadata = relationship('AgentMetadata')



class Relationship(CoreBase):
    """
    A relationship represents a connection between two entities in the knowledge graph.
    Like entities, relationships can have states that change over time/context.
    """
    __tablename__ = 'relationship'
    
    # Override creation source for relationships to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                         nullable=False, 
                         default=CreationSourceType.AI,
                         index=True)
    
    # Current overall status (derived from most recent state)
    current_status = Column(SQLEnum(RelationStatusType), 
                          nullable=False, 
                          default=RelationStatusType.ACTIVE,
                          index=True)
    
    # Core relationship fields
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey('entity.id'), nullable=False)
    source_entity = relationship(
        "Entity",
        foreign_keys=[source_entity_id],
        back_populates='relationships',
        overlaps="relationships",
        )
    
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey('entity.id'), nullable=False)
    target_entity = relationship(
        "Entity",
        foreign_keys=[target_entity_id],
        back_populates='relationships',
        overlaps="relationships",
        )
    
    direction = Column(SQLEnum(RelationDirectionType), nullable=False, index=True)
    
    # Type classification
    relationship_type = Column(SQLEnum(RelationType), nullable=False, index=True)
    subtype = Column(String(255), index=True)  # Optional more specific type
    additional_types = Column(ARRAY(String))   # Additional type classifications

    # Relationship States
    states = relationship(
        'RelationshipState', 
        back_populates='parent_relationship'
        )
