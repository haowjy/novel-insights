# novelinsights/models/presentation.py

from sqlalchemy import (
    Boolean,
    Column, 
    ForeignKey, 
    String, 
    DateTime, 
    Table, 
    UniqueConstraint, 
    Index, 
    Integer,
    event
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, object_session
from sqlalchemy import Enum as SQLEnum
from novelinsights.models.base import Base, SlugMixin, TemporalSnapshotMixin, CoreBase, CreationSourceType
from novelinsights.models.knowledge.entity import EntityType

"""

This file contains the SQLAlchemy models for representing articles in the system.
Articles are a collection of snapshots, each representing a different state of the article.

"""

# Association table for ordered content units
articlesnapshot_contentunit = Table(
    'article_content_unit',
    Base.metadata,
    Column('article_snapshot_id', UUID(as_uuid=True), 
           ForeignKey('article_snapshot.id'), primary_key=True),
    Column('content_unit_id', UUID(as_uuid=True), 
           ForeignKey('content_unit.id'), primary_key=True),
    Column('sequence', Integer),
    Column('source', SQLEnum(CreationSourceType)),
    UniqueConstraint('article_snapshot_id', 'sequence', 
                    name='uq_article_content_sequence')
)

# Association table for articles to entities
articlesnapshot_entitystate = Table(
    'articlesnapshot_entitystate',
    Base.metadata,
    Column('article_snapshot_id', UUID(as_uuid=True), ForeignKey('article_snapshot.id'), primary_key=True),
    Column('entity_state_id', UUID(as_uuid=True), ForeignKey('entity_state.id'), primary_key=True),
    Column('is_primary', Boolean, default=False),  # Optional: to mark the main subject if needed
)


class ArticleSnapshot(TemporalSnapshotMixin, SlugMixin, CoreBase):
    """
    An ArticleSnapshot represents a complete presentation state of content at a point in time.
    It references a ContentStructure (which organizes the content) but captures the specific
    state of that structure and its content units at generation time.
    
    Relationships:
    - Many ArticleSnapshots can reference one ContentStructure (parent or current)
    - Each ArticleSnapshot has exactly one parent and one current structure
    """
    __tablename__ = 'article_snapshot'
    
    # Simple back-reference to article
    article_id = Column(UUID(as_uuid=True), ForeignKey('article.id'), nullable=False)
    article = relationship('Article', back_populates="snapshots", foreign_keys=[article_id])
    
    # User tracking
    created_by_id = Column(UUID(as_uuid=True), 
                          ForeignKey('users.id'),
                          nullable=True)
    updated_by_id = Column(UUID(as_uuid=True), 
                          ForeignKey('users.id'),
                          nullable=True)
    
    # User relationships - names must match back_populates in User model
    creator = relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_articlesnapshots",
    )
    last_editor = relationship(
        "User",
        foreign_keys=[updated_by_id],
        back_populates="updated_articlesnapshots",
    )
    
    # Content units
    content_units = relationship(
        'ContentUnit',
        secondary=articlesnapshot_contentunit,
        order_by='article_content_unit.c.sequence'
    )
    
    # Entities
    entity_states = relationship(
        'EntityState',
        secondary=articlesnapshot_entitystate,
        order_by='articlesnapshot_entitystate.c.is_primary'
    )
    
    # Metadata
    generated_at = Column(DateTime)

    __table_args__ = (
        # Unique index for user-article combination
        Index(
            'ix_user_article_snapshot_unique',  # index name
            'article_id', 'created_by_id',
            unique=True,
            postgresql_where=created_by_id.isnot(None)  # Only apply when there is a creator
        ),
    )

class Article(SlugMixin, CoreBase):
    __tablename__ = 'article'
    
    # Core identity fields
    title = Column(String(255), nullable=False)
    type = Column(SQLEnum(EntityType), nullable=False)
    
    # Defer the foreign key constraint creation
    latest_snapshot_id = Column(UUID(as_uuid=True), 
                               ForeignKey('article_snapshot.id', 
                                        use_alter=True,
                                        name='fk_article_latest_snapshot'),
                               nullable=True)
    
    # Update the relationship to be more explicit
    snapshots = relationship(
        ArticleSnapshot,
        back_populates="article",
        foreign_keys=[ArticleSnapshot.article_id]  # Specify which foreign key to use
    )


@event.listens_for(Article, 'before_insert')
@event.listens_for(Article, 'before_update')
def generate_article_slug(mapper, connection, target):
    session = object_session(target)
    if session and target.title:
        target.slug = SlugMixin._make_unique_slug(
            session,
            Article,
            target.title,
            target.entity_id,
            getattr(target, 'id', None)
        )
        
@event.listens_for(ArticleSnapshot, 'before_insert')
@event.listens_for(ArticleSnapshot, 'before_update')
def generate_article_snapshot_slug(mapper, connection, target):
    session = object_session(target)
    if session and target.title:
        target.slug = SlugMixin._make_unique_slug(
            session,
            ArticleSnapshot,
            target.title,
            None,
            getattr(target, 'id', None)
        )