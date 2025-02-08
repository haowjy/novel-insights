# novelinsights/models/knowledge.py

# Standard library imports
from enum import Enum
# SQLAlchemy core imports
from sqlalchemy import (
    Column,
    Index,
    String,
    ForeignKey,
    Integer,
    Text,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import (
    UUID,     # For UUID field type
    JSONB,    # For JSON fields with binary storage
    ARRAY,    # For array fields
    TSVECTOR, # For text search
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from novelinsights.models.base import CreationSourceType, TemporalSnapshotMixin, CoreBase
from novelinsights.models.metadata.agent_metadata import AgentMetadata

#
#
#
# The following models are used to represent the knowledge graph.
# They are used to represent the entities and relationships in the world.
# It is all AI generated and is not manually created.
# 
#
#

class CoreNodeType(Enum):
    # Entities and Groups
    CHARACTER = "character"          # Individual beings/personas
    ORGANIZATION = "organization"    # Groups of any kind
    
    LOCATION = "location"           # Any kind of place or space
    ITEM = "item"                   # Physical or abstract objects
    CONCEPT = "concept"             # Ideas, systems, powers, theories
    CULTURE = "culture"             # Distinct societal patterns/practices
    
    # Temporal
    EVENT = "event"                 # Discrete occurrences
    TIME_PERIOD = "time_period"     # Temporal ranges
    
    # Narrative
    ARC = "arc"                     # Major narrative progressions
    THEME = "theme"                 # Recurring ideas or motifs
    
    OTHER = "other"                 # Other types not listed above


class Node(CoreBase):
    """
    A node is a single entity in the knowledge graph.
    It is the core of the knowledge graph and is used to represent entities in the world.
    Parent of node states that actually contain the knowledge.
    Usually created by an AI agent.
    """
    __tablename__ = 'node'
    
    # Override creation source for nodes to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                          nullable=False, 
                          default=CreationSourceType.AI,
                          index=True)
    
    # Core identity fields
    name = Column(String(255), nullable=False, index=True)
    core_type = Column(SQLEnum(CoreNodeType), nullable=False, index=True)
    
    # flexible type classification with more nuance
    optional_type = Column(String(255), index=True)
    additional_types = Column(ARRAY(String)) # Additional types or categories the AI has identified
    
    # Searchable fields
    ts_vector = Column(TSVECTOR) # name, optional_type, additional_types
    
    # Relationships
    # It's states over time
    states = relationship('NodeState', back_populates='node')
    
    # Relationships
    relationships = relationship(
        "NodeRelationship",
        primaryjoin="or_(Node.id==NodeRelationship.source_node_id, Node.id==NodeRelationship.target_node_id)",
    )
    
    __table_args__ = (
        Index('ix_node_ts_vector', 'ts_vector', postgresql_using='gin'),
    )

class NodeState(TemporalSnapshotMixin, CoreBase):
    """
    A node state is a collection of knowledge about a node.
    It is the child of a node and contains the actual knowledge about the node.
    """
    __tablename__ = 'node_state'
    
    # Override creation source for node_states to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                          nullable=False, 
                          default=CreationSourceType.AI,
                          index=True)
    
    # reference to the node that this state belongs to
    node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    node = relationship('Node', back_populates='states')
    
    # reference to the content units that this node state references from
    content_units = relationship(
        'ContentUnit', 
        back_populates='node_states',
        secondary='contentunit_nodestate'
    )
    
    # reference to the article snapshots that this node state references from
    article_snapshots = relationship(
        'ArticleSnapshot', 
        back_populates='node_states',
        secondary='articlesnapshot_nodestate'
    )
    
    # reference to the contexts that this node state references from
    contexts = relationship(
        'Context',
        back_populates='node_states',
        secondary='context_node_state'
    )
    
    # AI-generated fields
    importance = Column(Integer, comment="1-5, 1 being the most important")
    summary = Column(Text) # AI generated summary of the content unit
    
    # TODO: is this much conditional logic needed?
    knowledge = Column(JSONB, 
        # CheckConstraint("""
        #     (knowledge ? 'explicit') AND
        #     (knowledge ? 'implicit') AND
        #     (knowledge ? 'situational') AND
        #     (knowledge ? 'foundational')
        # """),
        comment="""
        {
            "explicit": {}, # Directly stated in text
            "implicit": {}, # AI-inferred knowledge
            "situational": {}, # Temporary/contextual information
            "foundational": {} # Core/persistent information
        }
        """
    )
    
    # Searchable fields
    ts_vector = Column(TSVECTOR) # summary, knowledge
    state_embedding = Column(Vector(1536))  # Adjust dimension based on model,
    
    __table_args__ = (
        Index('ix_node_state_ts_vector', 'ts_vector', postgresql_using='gin'),
        Index(
            'node_state_embedding_idx',
            state_embedding,
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'state_embedding': 'vector_cosine_ops'}
        )
    )
    
    # Agent history metadata if this node was created by an ai agent (nodes are always created by an agent)
    # one node to one agent metadata
    agent_metadata_id = Column(UUID(as_uuid=True), ForeignKey('agent_metadata.id'), nullable=False)
    agent_metadata = relationship(AgentMetadata)
