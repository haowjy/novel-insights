# novelinsights/models/knowledge.py

# Standard library imports
from enum import Enum

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

from novelinsights.models.base import Base, CreationSourceType, TemporalSnapshotMixin, CoreBase


# NEW: Define the association table for Relationship <--> Context
noderelationship_context = Table(
    "noderelationship_context",
    Base.metadata,
    Column("node_relationship_id", UUID(as_uuid=True), ForeignKey("node_relationship.id"), primary_key=True),
    Column("context_id", UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True),
    Column("source", SQLEnum(CreationSourceType))
)

# NEW: Define the association table for Relationship <--> ContentUnit
noderelationship_contentunit = Table(   
    "noderelationship_contentunit",
    Base.metadata,
    Column("node_relationship_id", UUID(as_uuid=True), ForeignKey("node_relationship.id"), primary_key=True),
    Column("content_unit_id", UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
    Column("source", SQLEnum(CreationSourceType))
)

class RelationshipDirection(Enum):
    OUTBOUND = "outbound"         # Relationship from source to target
    INBOUND = "inbound"           # Relationship from target to source
    BIDIRECTIONAL = "bidirectional"  # Mutual relationship

class RelationType(Enum):
    # Social/Personal
    FAMILY = "family"             # Family relationships
    FRIENDSHIP = "friendship"     # Friendships
    RIVALRY = "rivalry"           # Rivalries/enemies
    ROMANCE = "romance"           # Romantic relationships
    
    # Organizational
    MEMBERSHIP = "membership"     # Being part of organization/group
    LEADERSHIP = "leadership"     # Leading/commanding others
    ALLIANCE = "alliance"         # Alliances between groups/entities
    
    # Spatial/Physical
    LOCATION = "location"         # Physical relationships (contains, near)
    POSSESSION = "possession"     # Ownership/possession relationships
    
    # Abstract/Other
    KNOWLEDGE = "knowledge"       # Knowledge/awareness relationships
    INFLUENCE = "influence"       # Impact/effect relationships
    CAUSATION = "causation"      # Cause-effect relationships
    OTHER = "other"              # Other types

class RelationshipStatus(Enum):
    ACTIVE = "active"           # Currently valid relationship
    DORMANT = "dormant"         # Temporarily inactive (e.g., characters separated)
    BROKEN = "broken"           # Explicitly ended (e.g., breakup, betrayal)
    DECEASED = "deceased"       # One party died
    HISTORICAL = "historical"   # Past relationship, no longer current
    UNKNOWN = "unknown"         # Status unclear or not specified

class NodeRelationship(CoreBase):
    """
    A relationship represents a connection between two nodes in the knowledge graph.
    Like nodes, relationships can have states that change over time/context.
    """
    __tablename__ = 'node_relationship'
    
    # Override creation source for relationships to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                         nullable=False, 
                         default=CreationSourceType.AI,
                         index=True)
    
    # Current overall status (derived from most recent state)
    current_status = Column(SQLEnum(RelationshipStatus), 
                          nullable=False, 
                          default=RelationshipStatus.ACTIVE,
                          index=True)
    
    # Core relationship fields
    source_node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    target_node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    direction = Column(SQLEnum(RelationshipDirection), nullable=False, index=True)
    
    # Type classification
    relationship_type = Column(SQLEnum(RelationType), nullable=False, index=True)
    subtype = Column(String(255), index=True)  # Optional more specific type
    additional_types = Column(ARRAY(String))   # Additional type classifications
    
    # Relationships
    source_node = relationship("Node", foreign_keys=[source_node_id])
    target_node = relationship("Node", foreign_keys=[target_node_id])
    
    # Contexts
    contexts = relationship(
        'Context',
        back_populates="relationships",
        secondary='noderelationship_context'
    )
    content_units = relationship(
        'ContentUnit', 
        backref="relationships", 
        secondary='noderelationship_contentunit'
    )
    

class NodeRelationshipState(TemporalSnapshotMixin, CoreBase):
    """
    A relationship state represents the state of a relationship at a specific point
    in the content or context.
    """
    __tablename__ = 'node_relationship_state'
    
    # Override creation source for relationship_states to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                         nullable=False, 
                         default=CreationSourceType.AI,
                         index=True)
    
    node_relationship_id = Column(UUID(as_uuid=True), ForeignKey('node_relationship.id'), nullable=False)
        
    # AI-generated fields
    strength = Column(Integer, comment="1-5, 5 being the strongest connection")
    description = Column(Text)  # Brief description of the relationship state
    
     # If we need structured data about the relationship, keep it focused on the connection
    properties = Column(JSONB, 
        comment="""
        {
            "status": str,      # e.g., "active", "strained", "broken"
            "dynamics": str,    # e.g., "supportive", "antagonistic"
            "evidence": list    # References to supporting content
        }
        """
    )
    
    # Agent metadata if this state was created by an AI agent
    agent_metadata = relationship('AgentMetadata', backref="relationship_state")

    # Status at this point in content
    status = Column(SQLEnum(RelationshipStatus), 
                   nullable=False, 
                   default=RelationshipStatus.ACTIVE)
    
    # Structured data about the state change
    transition = Column(JSONB,
        comment="""
        {
            "type": str,          # e.g., "breakup", "death", "separation"
            "cause": str,         # Reason for status change
            "permanence": str,    # "temporary", "permanent", "unknown"
            "initiator_id": uuid  # Which node initiated the change (if applicable)
        }
        """
    )
    


