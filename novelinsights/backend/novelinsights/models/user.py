from sqlalchemy import Column, Integer, String, Text, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from .base import TimestampedBase

class UserType(str, SQLEnum):
    """Types of users in the system"""
    HUMAN = "human"        # Regular human users
    AI = "ai"             # AI systems (e.g., Claude)
    SYSTEM = "system"     # System automated processes

class User(TimestampedBase):
    """Model for tracking both human users and AI agents"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    type = Column(SQLEnum(UserType), nullable=False)
    
    # Human user specific fields
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))  # For human users only
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # AI specific fields
    ai_model = Column(String(255))  # e.g., "claude-3-opus-20240229"
    ai_provider = Column(String(255))  # e.g., "anthropic"
    
    # Optional profile information
    display_name = Column(String(255))
    bio = Column(Text)
    preferences = Column(JSONB)  # Store user preferences as JSON
    
    # Relationships with content
    created_articles = relationship(
        "Article",
        foreign_keys="[Article.created_by_id]",
        back_populates="creator"
    )
    updated_articles = relationship(
        "Article",
        foreign_keys="[Article.updated_by_id]",
        back_populates="last_editor"
    )
    article_versions = relationship(
        "ArticleVersion", 
        foreign_keys="[ArticleVersion.author_id]",
        back_populates="author"
    )
    reviewed_versions = relationship(
        "ArticleVersion",
        foreign_keys="[ArticleVersion.reviewer_id]",
        back_populates="reviewer"
    )

    def __repr__(self):
        return f"<User {self.username} ({self.type})>"
