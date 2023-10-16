from sqlalchemy.orm import Session
import pytest
from app.models.book import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from app.api.endpoints.book import *
from pymongo import MongoClient



# Setup necessary data and environment
@pytest.fixture(scope="module")
def db_engine():
    # Assuming that necessary environment variables are set
    client = MongoClient(DATABASE_URL)
    db_engine = client.get_database()
    return db_engine


def test_recreate_database(db_uri: str):
    # Connect to the database
    client = MongoClient(db_uri)

    try:
        # Drop the database
        client.drop_database('myDatabase')
        
        # Recreate the database
        recreate_database()
    except Exception as e:
        pytest.fail(f"Recreate database method failed with error: {e}")
    finally:
        # Close the connection
        client.close()


# The import that needed
from sqlalchemy import create_engine
