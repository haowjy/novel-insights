# novelinsights/models/core.py

from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from novelinsights.models.base import CoreBase
from novelinsights.models.presentation.article import ArticleSnapshot

class User(CoreBase):
    """Model for human users"""
    __tablename__ = "users"
    
    firebase_uid = Column(String(128), unique=True)  # Add Firebase UID
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), unique=True)
    
    # Auth related
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    
    # Profile information
    display_name = Column(String(255))
    photo_url = Column(String(1024))
    bio = Column(Text)
    preferences = Column(JSONB)
    
    # Article relationships
    created_articlesnapshots = relationship(
        ArticleSnapshot,
        foreign_keys=ArticleSnapshot.created_by_id,
        back_populates="creator",
    )   
    updated_articlesnapshots = relationship(
        ArticleSnapshot,
        foreign_keys=[ArticleSnapshot.updated_by_id],
        back_populates="last_editor",
    )

    def __repr__(self):
        return f"<User {self.username}>"
