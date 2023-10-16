from sqlalchemy.orm import Session
import pytest
from app.models.book import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import engine
from app.api.endpoints.book import *


# Setup necessary data and environment
@pytest.fixture(scope="module")
def db_engine() -> engine:
    # Assuming that necessary environment variables are set
    db_engine = create_engine(DATABASE_URL)
    return db_engine


# Test if the function recreates the database successfully without throwing errors
def test_recreate_database(db_engine: engine):
    # Creating a SessionLocal class which is a factory to create new Session instances
    session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    # Connect to the database
    connection = db_engine.connect()
    # Begin a non-ORM transaction
    transaction = connection.begin()
    # Bind an individual Session to the connection
    test_session = session(bind=connection)
    try:
        recreate_database()
    except Exception as e:
        pytest.fail(f"Recreate database method failed with error: {e}")
    finally:
        # Roll back the encapsulating transaction
        transaction.rollback()
        # Close the session
        test_session.close()
        # Close the connection
        connection.close()


# The import that needed
from sqlalchemy import create_engine
