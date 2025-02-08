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


"""

This file contains the SQLAlchemy models for representing relationships in the knowledge graph.

Key components:
- Association tables for many-to-many relationships between relationships and contexts/content units
- Enums defining relationship directions, types, and statuses
- Models for relationship states and relationships themselves

The models are used to represent connections between nodes in the knowledge graph, capturing:
- Directionality (outbound, inbound, bidirectional)
- Type (family, friendship, rivalry, etc.)
- Status (active, dormant)
- Temporal snapshots of relationship states
- Associations with content units and contexts

These models form the core of the relationship representation in the knowledge graph system.

"""

# NEW: Define the association table for Relationship <--> Context
noderelationship_context = Table(
    "noderelationship_context",
    Base.metadata,
    Column('node_relationship_id', UUID(as_uuid=True), ForeignKey("node_relationship.id"), primary_key=True),
    Column('context_id', UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True),
    Column('source', SQLEnum(CreationSourceType))
)

# NEW: Define the association table for Relationship <--> ContentUnit
noderelationship_contentunit = Table(   
    "noderelationship_contentunit",
    Base.metadata,
    Column('node_relationship_id', UUID(as_uuid=True), ForeignKey("node_relationship.id"), primary_key=True),
    Column('content_unit_id', UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
    Column('source', SQLEnum(CreationSourceType))
)

class RelationDirectionType(Enum):
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

class RelationStatusType(Enum):
    ACTIVE = "active"           # Currently valid relationship
    DORMANT = "dormant"         # Temporarily inactive (e.g., characters separated)
    BROKEN = "broken"           # Explicitly ended (e.g., breakup, betrayal)
    DECEASED = "deceased"       # One party died
    HISTORICAL = "historical"   # Past relationship, no longer current
    UNKNOWN = "unknown"         # Status unclear or not specified

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
    node_relationship = relationship('NodeRelationship', back_populates='states')

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
    current_status = Column(SQLEnum(RelationStatusType), 
                          nullable=False, 
                          default=RelationStatusType.ACTIVE,
                          index=True)
    
    # Core relationship fields
    source_node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    source_node = relationship(
        "Node",
        foreign_keys=[source_node_id],
        back_populates='relationships',
        overlaps="relationships",
        )
    
    target_node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    target_node = relationship(
        "Node",
        foreign_keys=[target_node_id],
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
        'NodeRelationshipState', 
        back_populates='node_relationship'
        )
