import pytest

from app.api.dependencies import *
from sqlalchemy.orm import sessionmaker


import pytest
from sqlalchemy import create_engine

# Importing necessary objects and functions for the test
from sqlalchemy import create_engine

# Pytest for the get_db function


# Test fixture to create a database engine
@pytest.fixture(scope="module")
def test_engine():
    # Define the database connection string
    connection_string = (
        "postgresql://refactorybot:22r)pGKLcaeP@"
        "refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703603283683"
    )
    # Create a database engine
    engine = create_engine(connection_string)
    return engine


# Test fixture to create a TestingSessionLocal using the test engine
@pytest.fixture(scope="module")
def TestingSessionLocal(test_engine):
    """Create a sessionmaker for testing purposes."""
    _TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    return _TestingSessionLocal


# Test that 'get_db' can be called successfully
def test_get_db_execution(TestingSessionLocal, monkeypatch):
    # Use monkeypatch to override the SessionLocal with our TestingSessionLocal
    monkeypatch.setattr("app.db.database.SessionLocal", TestingSessionLocal)

    # Use get_db to get a database session
    db_generator = get_db()
    db_session = next(db_generator)
    assert db_session is not None, "get_db did not return a database session."
    db_session.close()
