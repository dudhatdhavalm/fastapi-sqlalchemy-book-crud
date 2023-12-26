import pytest

from app.api.dependencies import *
from sqlalchemy.orm import sessionmaker


import pytest
from sqlalchemy import create_engine

from sqlalchemy import create_engine
from pymongo import MongoClient
from app.api.dependencies import get_db



@pytest.fixture(scope="module")
def test_engine():
    connection_string = (
        "postgresql://refactorybot:22r)pGKLcaeP@"
        "refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703603283683"
    )
    engine = create_engine(connection_string)
    return engine


@pytest.fixture(scope="module")
def TestingSessionLocal(test_engine):
    """Create a sessionmaker for testing purposes."""
    _TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    return _TestingSessionLocal


# You may need to update the 'app.db.database.SessionLocal' to the correct path where get_db is defined
# Also, ensure 'TestingMongoClient' returns a PyMongo client pointing to a test database

def test_get_db_execution(TestingMongoClient, monkeypatch):
    # this could be 'app.db.get_db' depending on how the get_db function is imported
    monkeypatch.setattr("app.api.dependencies.get_db", TestingMongoClient)
    
    db_generator = get_db()
    db_client = next(db_generator)
    # Assuming 'get_db' returns a db client, otherwise you'd check for a specific database or collection
    assert db_client is not None, "get_db did not return a database client."
    # If there is specific clean-up needed, do it here. Otherwise, the garbage collector handles it.
    # db_client.close()  # typically, you wouldn't call close() manually in PyMongo
