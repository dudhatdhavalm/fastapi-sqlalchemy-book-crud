import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine


import pytest
from app.db.database import Base, SessionLocal
from app.api.dependencies import *
from pymongo import MongoClient



# Define a fixture for initializing and tearing down a test database
@pytest.fixture(scope="module")
def test_db():
    # We're using MongoDB for testing
    TEST_DATABASE_URL = "mongodb://localhost:27017/"

    # Create test client
    client = MongoClient(TEST_DATABASE_URL)

    # Create a new database for each test
    def get_test_db():
        db = client['test_db']
        return db

    yield get_test_db()  # Provide the fixture value

    # Teardown
    client.drop_database('test_db')


def test_get_db(test_db):
    """Test get_db function if it doesn't throw errors when it's executed"""
    client = None
    try:
        client = next(get_db())
    except Exception as e:
        pytest.fail(f"An error occurred while executing get_db: {e}")

    assert client is not None, "No client was yielded by get_db function"
    assert isinstance(
        client, MongoClient
    ), "get_db function did not return a MongoClient instance"
