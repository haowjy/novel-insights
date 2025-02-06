# novelinsights/models/content.py

from sqlalchemy import Column, ForeignKey, Table, Text, Integer, UniqueConstraint, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from novelinsights.models.base import Base, CoreBase, CreationSourceType

# Content Unit Association Tables
contentunit_contentstructure = Table(
    "contentunit_contentstructure",
    Base.metadata,
    Column("content_structure_id", UUID(as_uuid=True), ForeignKey("content_structure.id"), primary_key=True),
    Column("content_unit_id", UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
    Column("source", SQLEnum(CreationSourceType))
)

contentunit_node = Table(
       "contentunit_node",
       Base.metadata,
       Column("node_id", UUID(as_uuid=True), ForeignKey("node.id"), primary_key=True),
       Column("content_unit_id", UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
       Column("source", SQLEnum(CreationSourceType))
)

class ContentUnit(CoreBase):
    __tablename__ = 'content_unit'
    
    content = Column(Text)
    context_id = Column(UUID(as_uuid=True), ForeignKey('context.id'))
    
    # Structure fields
    content_structure_id = Column(UUID(as_uuid=True), ForeignKey('content_structure.id'), unique=True)
    sequence = Column(Integer, nullable=True)  # Sequence of the unit within the structure
    
    # Search fields
    ts_vector = Column(TSVECTOR)
    content_embedding = Column(Vector(1536))  # Adjust dimension based on model

    # Relationships
    structure = relationship(
        'ContentStructure', 
        backref='content_units',
        secondary='contentunit_contentstructure')
    
    contexts = relationship(
        'Context', 
        backref='content_units', 
        secondary='context_contentunit')
    
    nodes = relationship(
        'Node',
        backref='content_units',
        secondary='contentunit_node'
    )
    
    article_snapshots = relationship(
        "ArticleSnapshot",
        back_populates="content_units",
        secondary='article_content_unit'
    )
    
    __table_args__ = (
        UniqueConstraint('content_structure_id', 'sequence', 
                        name='uq_unit_structure_sequence',
                        deferrable=True,  # Allow temporary violations during transactions
                        initially='DEFERRED'
                        ),
        
        Index('ix_content_structure_id', 'content_structure_id'),  # Index for joins and constraint checks
        Index('ix_context_id', 'context_id'),  # Index for joins involving context_id
        Index('ix_content_unit_ts_vector', 'ts_vector'),  # Changed index name to be table-specific
        Index(
            'content_unit_embedding_idx',
            content_embedding,
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'content_embedding': 'vector_cosine_ops'}
        )
    )
