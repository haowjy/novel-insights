import pytest
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from novelinsights.models.base import Base

load_dotenv()

@pytest.fixture(scope="session")
def db_session():
    """Create a database session for testing using PostgreSQL in Docker."""
    # Database URL from environment variable, default to a standard value
    db_url = os.environ.get("DATABASE_URL", f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:"
    f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}@localhost:"
    f"{os.getenv('POSTGRES_PORT', '5432')}/"
    f"{os.getenv('POSTGRES_DB', 'novelinsights')}")
    
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()