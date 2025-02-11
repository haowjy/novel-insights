from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel

from novelinsights.models.knowledge.entity import EntityType
from novelinsights.schemas.base import CoreBase, BaseConfig, TemporalSnapshotBase, SlugBase

class ArticleSnapshotBase(CoreBase, TemporalSnapshotBase, SlugBase):
    """Base schema for article snapshot without ID fields"""
    article_id: UUID
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    generated_at: Optional[datetime] = None

# TODO: Add create schema

class ArticleSnapshotCreate(ArticleSnapshotBase):
    """Schema for creating a new article snapshot"""
    pass

# TODO

class ArticleSnapshot(ArticleSnapshotBase):
    """Complete article snapshot schema with all fields"""
    pass

class ArticleSnapshotUpdate(BaseConfig):
    """Schema for updating an article snapshot"""
    created_by_id: Optional[UUID] = None
    updated_by_id: Optional[UUID] = None
    generated_at: Optional[datetime] = None
    parent_structure_id: Optional[UUID] = None
    current_structure_id: Optional[UUID] = None









class ArticleBase(CoreBase, SlugBase):
    """Base schema for article without ID fields"""
    title: str
    type: EntityType
    latest_snapshot_id: Optional[UUID] = None

    class Config:
        from_attributes = True

# TODO: Add create schema

class ArticleCreate(ArticleBase):
    """Schema for creating a new article"""
    pass

# TODO

class Article(ArticleBase):
    """Complete article schema with all fields"""
    pass

class ArticleUpdate(BaseConfig):
    """Schema for updating an article"""
    title: Optional[str] = None
    type: Optional[EntityType] = None
    latest_snapshot_id: Optional[UUID] = None

    class Config:
        from_attributes = True 