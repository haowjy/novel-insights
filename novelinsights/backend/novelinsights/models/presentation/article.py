# novelinsights/models/presentation.py

from sqlalchemy import (
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
from novelinsights.models.knowledge.node import CoreNodeType


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

class Article(SlugMixin, CoreBase):
    __tablename__ = 'article'
    
    # Core identity fields
    node_id = Column(UUID(as_uuid=True), ForeignKey('node.id'), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(SQLEnum(CoreNodeType), nullable=False)
    
    # Defer the foreign key constraint creation
    current_snapshot_id = Column(UUID(as_uuid=True), 
                               ForeignKey('article_snapshot.id', 
                                        use_alter=True,
                                        name='fk_article_current_snapshot'),
                               nullable=True)
    
    # Only need this one relationship
    snapshots = relationship("ArticleSnapshot", back_populates="article")
    node = relationship('Node', backref='articles')
    

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
    
    article_id = Column(UUID(as_uuid=True), ForeignKey('article.id'), nullable=False)
    
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
        back_populates="created_snapshots"
    )
    last_editor = relationship(
        "User",
        foreign_keys=[updated_by_id],
        back_populates="updated_snapshots"
    )
    
    article_structure_id = Column(UUID(as_uuid=True), 
                                  ForeignKey('content_structure.id'), 
                                  nullable=False)
    # Article Content Structure
    # This is the structure of the article as it is currently presented
    # separate from the official content structure of the book or publication
    # This is just how an article is "written" if it were written by the author
    # one article structure to one article
    articlesnapshot_structure = relationship('ContentStructure', 
                                   foreign_keys=[article_structure_id])
    
    # Content units
    content_units = relationship(
        'ContentUnit',
        secondary=articlesnapshot_contentunit,
        order_by='article_content_unit.c.sequence'
    )
    
    # Metadata
    generated_at = Column(DateTime)
    
    # Simple back-reference to article
    article = relationship(Article, back_populates="snapshots")

    __table_args__ = (
        # Unique index for user-article combination
        Index(
            'ix_user_article_snapshot_unique',  # index name
            'article_id', 'created_by_id',
            unique=True,
            postgresql_where=created_by_id.isnot(None)  # Only apply when there is a creator
        ),
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
            target.node_id,
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