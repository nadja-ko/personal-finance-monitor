import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.database.connection import Base


@pytest.fixture
def db_session() -> Session:
    """
    Create a new database session for testing.
    Every test will use an in-memory SQLite database,
    which is created and destroyed for each test.
    """
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session
