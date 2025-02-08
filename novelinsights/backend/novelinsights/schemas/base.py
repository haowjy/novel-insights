from datetime import datetime

from uuid import UUID
from pydantic import BaseModel

from novelinsights.models.base import CreationSourceType

class BaseConfig(BaseModel):
    class Config:
        from_attributes = True
        
class CoreBase(BaseConfig):
    """
    Base schema that adds UUID, creation and update timestamps.
    Mirrors the CoreBase model from the database.
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    creation_source: CreationSourceType

class TemporalSnapshotBase(BaseConfig):
    """
    Base schema for temporal snapshots.
    Mirrors the TemporalSnapshotMixin from the database.
    """
    parent_structure_id: UUID
    current_structure_id: UUID

class SlugBase(BaseConfig):
    """
    Base schema for slugged content.
    Mirrors the SlugMixin from the database.
    """
    slug: str
    