import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.database.connection import Base
from backend.database.session import get_db
from backend.main import app


@pytest.fixture
def db_session() -> Session:
    """
    Create a new database session for testing.

    Every test uses an in-memory SQLite database that is
    created and destroyed for each test.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """
    Create a FastAPI test client using the test database.
    """

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
