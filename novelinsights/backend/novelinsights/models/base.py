from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime, UTC

Base = declarative_base()

class TimestampedBase(Base):
    """Abstract base class that adds creation and update timestamps to models."""
    __abstract__ = True
    created_at = Column(DateTime, 
                       default=datetime.now(UTC),
                       nullable=False,
                       comment="When this record was first created")
    
    updated_at = Column(DateTime,
                       default=datetime.now(UTC),
                       onupdate=datetime.now(UTC),
                       nullable=False,
                       comment="When this record was last modified")