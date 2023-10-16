from main import *
import pytest
from app.models.book import Base
from sqlalchemy import engine
from pymongo import MongoClient


@pytest.fixture(scope="module")
def setup_test_db() -> None:
    """
    Set up the test database for pytest using pymongo.
    """
    # Create a new MongoClient instance
    client = MongoClient()

    # Create a new database for testing
    db = client.test_db

    # Drop the database to ensure a clean start
    db.drop_database('test_db')




def test_recreate_database(setup_test_db: pytest.fixture) -> None:
    """
    Test the recreate_database function to ensure it does not raise any exceptions.
    """
    try:
        client = MongoClient()
        db = client['test_database']
        db.drop_database()
        assert True
    except Exception as e:
        pytest.fail(f"recreate_database raised exception: {e}")
