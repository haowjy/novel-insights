# novelinsights/backend/novelinsights/models/content/context.py

from enum import Enum

from sqlalchemy import Column, ForeignKey, Index, String, Text, Integer, Table, Enum as SQLEnum, UniqueConstraint, event
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, object_session

from novelinsights.models.base import Base, SlugMixin, CoreBase, CreationSourceType


# Context Association Tables
context_content_structure = Table(
    'context_content_structure',
    Base.metadata,
    Column('context_id', UUID(as_uuid=True), 
           ForeignKey('context.id'), primary_key=True),
    Column('content_structure_id', UUID(as_uuid=True), 
           ForeignKey('content_structure.id'), primary_key=True),
    Column('source', SQLEnum(CreationSourceType))
)

context_contentunit = Table(
    "context_contentunit",
    Base.metadata,
    Column("context_id", UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True),
    Column("content_unit_id", UUID(as_uuid=True), ForeignKey("content_unit.id"), primary_key=True),
    Column("source", SQLEnum(CreationSourceType))
)

context_node = Table(
       "context_node",
       Base.metadata,
       Column("context_id", UUID(as_uuid=True), ForeignKey("context.id"), primary_key=True),
       Column("node_id", UUID(as_uuid=True), ForeignKey("node.id"), primary_key=True),
       Column("source", SQLEnum(CreationSourceType))
)

class ContextScope(Enum):
    GLOBAL = "global"           # Applies to entire work
    STRUCTURAL = "structural"   # Applies to specific content structures
    CONTENT_UNIT = "content_unit" # Applies to specific content units

class ContextType(Enum):
    THEME = "theme"
    POV = "pov"
    AUTHOR_NOTE = "author_note"
    WORLDBUILDING = "worldbuilding"
    WRITING_GUIDANCE = "writing_guidance"
    OTHER = "other"

class Context(SlugMixin, CoreBase):
    __tablename__ = 'context'
    
    # Core fields
    type = Column(SQLEnum(ContextType), nullable=False)
    scope = Column(SQLEnum(ContextScope), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    
    # Metadata
    properties = Column(JSONB)
    sequence = Column(Integer, comment="Optional ordering within same type/scope")
    
    # Relationships
    structures = relationship(
        'ContentStructure', 
        backref="contexts", 
        secondary='context_content_structure',
    )
    content_units = relationship(
        'ContentUnit', 
        backref="contexts", 
        secondary='context_contentunit',
    )
    nodes = relationship(
        'Node',
        backref='contexts', 
        secondary='context_node',
    )
    relationships = relationship(
        'NodeRelationship',
        back_populates="contexts",
        secondary='noderelationship_context',
    )
    
    __table_args__ = (
        UniqueConstraint('slug', name='unique_context_slug'),
        Index('idx_context_type_scope_seq', 'type', 'scope', 'sequence'),
    )

# Event listeners for each model
@event.listens_for(Context, 'before_insert')
@event.listens_for(Context, 'before_update')
def generate_context_slug(mapper, connection, target):
    session = object_session(target)
    if session and target.title:
        target.slug = SlugMixin._make_unique_slug(
            session,
            Context,
            target.title,
            None,  # No parent for books
            getattr(target, 'id', None)
        )
