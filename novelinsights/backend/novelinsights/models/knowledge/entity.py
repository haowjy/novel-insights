# novelinsights/models/knowledge.py

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

from novelinsights.models.base import TemporalSnapshotMixin, CoreBase
from novelinsights.models.metadata.agent_metadata import AgentMetadata
from novelinsights.types.knowledge import SignificanceLevel, EntityType
from novelinsights.types.core import CreationSourceType
"""

The following models are used to represent the knowledge graph.
They are used to represent the entities and relationships in the world.
It is all AI generated and is not manually created.

"""

class EntityState(TemporalSnapshotMixin, CoreBase):
    """
    An entity state is a collection of knowledge about an entity.
    It is the child of an entity and contains the actual knowledge about the entity.
    """
    __tablename__ = 'entity_state'
    
    # Override creation source for entity_states to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                          nullable=False, 
                          default=CreationSourceType.AI,
                          index=True)
    
    # reference to the entity that this state belongs to
    entity_id = Column(UUID(as_uuid=True), ForeignKey('entity.id'), nullable=False)
    entity = relationship('Entity', back_populates='states')
    
    # reference to the content units that this entity state references from
    content_units = relationship(
        'ContentUnit', 
        back_populates='entity_states',
        secondary='contentunit_entitystate'
    )
    
    # reference to the article snapshots that this entity state references from
    article_snapshots = relationship(
        'ArticleSnapshot', 
        back_populates='entity_states',
        secondary='articlesnapshot_entitystate'
    )
    
    # reference to the contexts that this entity state references from
    contexts = relationship(
        'Context',
        back_populates='entity_states',
        secondary='context_entity_state'
    )
    
    # AI-generated fields
    importance = Column(SQLEnum(SignificanceLevel), comment="Importance of the entity to the story")
    summary = Column(Text) # AI generated summary of the entity
    
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
        Index('ix_entity_state_ts_vector', 'ts_vector', postgresql_using='gin'),
        Index(
            'entity_state_embedding_idx',
            state_embedding,
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'state_embedding': 'vector_cosine_ops'}
        )
    )
    
    # Agent history metadata if this entity was created by an ai agent (entities are always created by an agent)
    # one entity to one agent metadata
    agent_metadata_id = Column(UUID(as_uuid=True), ForeignKey('agent_metadata.id'), nullable=False)
    agent_metadata = relationship(AgentMetadata)



class Entity(CoreBase):
    """
    An entity is a single entity in the knowledge graph.
    It is the core of the knowledge graph and is used to represent entities in the world.
    Parent of entity states that actually contain the knowledge.
    Usually created by an AI agent.
    """
    __tablename__ = 'entity'
    
    # Override creation source for entities to default to AI
    creation_source = Column(SQLEnum(CreationSourceType), 
                          nullable=False, 
                          default=CreationSourceType.AI,
                          index=True)
    
    # Core identity fields
    name = Column(String(255), nullable=False, index=True)
    entity_type = Column(SQLEnum(EntityType), nullable=False, index=True)
    
    # flexible type classification with more nuance
    optional_type = Column(String(255), index=True)
    additional_types = Column(ARRAY(String)) # Additional types or categories the AI has identified
    
    # Searchable fields
    ts_vector = Column(TSVECTOR) # name, optional_type, additional_types
    
    # Relationships
    # It's states over time
    states = relationship('EntityState', back_populates='entity')
    
    # Relationships
    relationships = relationship(
        "Relationship",
        primaryjoin="or_(Entity.id==Relationship.source_entity_id, Entity.id==Relationship.target_entity_id)",
        overlaps="relationships"
    )
    
    __table_args__ = (
        Index('ix_entity_ts_vector', 'ts_vector', postgresql_using='gin'),
    )
