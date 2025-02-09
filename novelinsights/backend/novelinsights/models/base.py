# novelinsights/backend/novelinsights/models/base.py

from datetime import datetime, UTC
from uuid import uuid4
from typing import Optional
from unidecode import unidecode
import re

from sqlalchemy import UUID, Column, DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import  declared_attr, declarative_base, Mapped, mapped_column, relationship

from novelinsights.types.core import CreationSourceType

Base = declarative_base()

class CoreBase(Base):
    """
    Abstract base class that adds a UUID primary key, creation and update timestamps to models.
    
    All models inheriting from this base will automatically have:
    - A UUID primary key field 'id'
    - created_at and updated_at timestamps that are managed by SQLAlchemy
    - A creation_source field indicating whether it was created with a human in the loop or AI
    """
    __abstract__ = True
    
    # UUID primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True),
                       default=datetime.now(UTC),
                       nullable=False,
                       index=True,  # Add index for common queries
                       comment="When this record was first created")
    
    updated_at = Column(DateTime(timezone=True),  # Explicit timezone handling
                       default=datetime.now(UTC),
                       onupdate=datetime.now(UTC),
                       nullable=False,
                       index=True,
                       comment="When this record was last modified")
    
    creation_source = Column(SQLEnum(CreationSourceType), 
                          nullable=False, 
                          index=True)  # Index if you frequently filter by source

class TemporalSnapshotMixin(object):
    """
    Mixin that adds structure references to models.
    References a temporal structure (e.g. book, chapter, section, etc.) via the parent_structure_id.
    and points to a child structure (e.g. chapter, section, etc.) via the current_structure_id.
    NOTE: you cannot access the fields from content_structure directly if you are using this mixin.
    """
    
    # Structure references (Many-to-One)
    # Example: parent = Book, current = Chapter
    # No information after this current chapter should be included
    @declared_attr
    def parent_structure_id(cls):
        return Column(UUID(as_uuid=True), 
                     ForeignKey('content_structure.id'), 
                     nullable=False)
    
    @declared_attr
    def current_structure_id(cls):
        return Column(UUID(as_uuid=True), 
                     ForeignKey('content_structure.id'), 
                     nullable=False)
    
    @declared_attr
    def parent_structure(cls):
        return relationship('ContentStructure', 
                          foreign_keys=[getattr(cls, 'parent_structure_id')])
    
    @declared_attr
    def current_structure(cls):
        return relationship('ContentStructure', 
                          foreign_keys=[getattr(cls, 'current_structure_id')])
        

class SlugMixin:
    @declared_attr
    def slug(self) -> Mapped[str]:
        return mapped_column(String(255), unique=False, nullable=False)  # unique=False for scoped slugs

    @staticmethod
    def _generate_slug(text: str) -> str:
        text = unidecode(text).lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')

    @staticmethod
    def _make_unique_slug(session, model, text: str, parent_id: Optional[int] = None, id: Optional[int] = None) -> str:
        slug = SlugMixin._generate_slug(text)
        original_slug = slug
        count = 1
        
        while True:
            query = session.query(model).filter(
                model.slug == slug,
                model.parent_id == parent_id
            )
            if id:
                query = query.filter(model.id != id)
            
            exists = query.first()
            if not exists:
                break
            
            slug = f"{original_slug}-{count}"
            count += 1
        return slug