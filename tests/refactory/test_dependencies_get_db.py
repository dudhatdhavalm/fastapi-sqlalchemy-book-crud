import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine


import pytest
from app.db.database import Base, SessionLocal
from app.api.dependencies import *


# Define a fixture for initializing and tearing down a test database
@pytest.fixture(scope="module")
def test_db():
    # We're using SQLite for testing
    TEST_DATABASE_URL = "sqlite:///:memory:"

    # Create test engine
    engine = create_engine(TEST_DATABASE_URL)

    # Create tables in the database
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    def get_test_session():
        session = Session(bind=engine)
        return session

    # Use the new function as the session factory
    SessionLocal = get_test_session

    yield SessionLocal  # Provide the fixture value

    # Teardown
    Base.metadata.drop_all(bind=engine)


def test_get_db(test_db):
    """Test get_db function if it doesn't throw errors when it's executed"""
    session = None
    try:
        session = next(get_db())
    except Exception as e:
        pytest.fail(f"An error occurred while executing get_db: {e}")

    assert session is not None, "No session was yielded by get_db function"
    assert isinstance(
        session, Session
    ), "get_db function did not return a database session"
