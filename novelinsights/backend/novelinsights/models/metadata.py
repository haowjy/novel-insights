from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import TimestampedBase

class Genre(TimestampedBase):
    """
    Represents a broad category or tradition of storytelling.
    Genres can have multiple related genres, reflecting how modern stories
    often blend different genre elements.
    """
    __tablename__ = "genres"
    
    # Define the junction tables within the relevant class
    _genre_relationships = Table(
        'genre_relationships',
        TimestampedBase.metadata,
        Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
        Column('related_genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
    )

    _book_genres = Table(
        'book_genres',
        TimestampedBase.metadata,
        Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
        Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
    )
    
    # Model columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships using the junction tables defined above
    books = relationship(
        "Book",
        secondary=_book_genres,
        back_populates="genres"
    )
    
    related_genres = relationship(
        'Genre',
        secondary=_genre_relationships,
        primaryjoin='Genre.id == genre_relationships.c.genre_id',
        secondaryjoin='Genre.id == genre_relationships.c.related_genre_id',
        back_populates='related_genres'
    )
    
    def __repr__(self):
        return f"<Genre {self.name}>"


class TagCategory(TimestampedBase):
    """
    Represents a broad classification for types of tags. This helps organize tags
    into meaningful groups that serve different purposes in describing stories.
    
    For example:
    - Plot Elements (time travel, magic systems)
    - Character Archetypes (anti-hero, wise mentor)
    - Themes (redemption, coming of age)
    - Story Structure (non-linear narrative, frame story)
    - Setting Elements (post-apocalyptic, urban fantasy)
    """
    __tablename__ = "tag_categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Tags belonging to this category
    tags = relationship("Tag", back_populates="category")
    
    def __repr__(self):
        return f"<TagCategory {self.name}>"
    
class Tag(TimestampedBase):
    """
    Represents specific elements, themes, or features that appear in stories.
    Each tag belongs to a specific category that indicates its role in describing
    a story's content.
    """
    __tablename__ = "tags"
    
    _tag_relationships = Table(
        'tag_relationships',
        TimestampedBase.metadata,
        Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
        Column('related_tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
    )

    _book_tags = Table(
        'book_tags',
        TimestampedBase.metadata,
        Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
    )
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Replace the string category with a proper foreign key relationship
    category_id = Column(Integer, ForeignKey('tag_categories.id'), nullable=False)
    category = relationship("TagCategory", back_populates="tags")
    
    books = relationship("Book", secondary=_book_tags, back_populates="tags")
    related_tags = relationship(
        'Tag',
        secondary=_tag_relationships,
        primaryjoin='Tag.id == tag_relationships.c.tag_id',
        secondaryjoin='Tag.id == tag_relationships.c.related_tag_id',
        back_populates='related_tags'
    )
    
    def __repr__(self):
        return f"<Tag {self.name}>"