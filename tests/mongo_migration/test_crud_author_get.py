from sqlalchemy.orm import sessionmaker

import pytest
from sqlalchemy import create_engine

from app.crud.crud_author import CRUDAuthor
from sqlalchemy.exc import SQLAlchemyError


from unittest.mock import MagicMock
from unittest.mock import MagicMock
from app.models.author import Author

from app.crud.crud_author import *
from pymongo import MongoClient
from pymongo.collection import Collection
from unittest.mock import MagicMock, patch

# Replace connection string with the appropriate URI for your MongoDB instance
MONGO_URI = 'mongodb://localhost:27017/'


class _BaseMock:
    query = MagicMock()




class _QueryMock:
    def offset(self, num):
        return self

    def limit(self, num):
        return self

    def all(self):
        return []


DATABASE_URI = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"


@pytest.fixture(scope="module")
def db_engine():
    return create_engine(DATABASE_URI)


@pytest.fixture(scope="module")
def db_session_factory(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    return SessionLocal


# Assuming you have an instance of MongoClient to connect to the MongoDB database and need to get a collection.
@pytest.fixture(scope="function")
def crud_author(mongo_client):
    collection = mongo_client['your_database']['author_collection']
    return CRUDAuthor(collection)


# Fixture to create a database session
@pytest.fixture(scope="function")
def db_session():
    client = MongoClient(MONGO_URI)
    # Assuming the database is named 'test_database'
    db = client.test_database
    try:
        yield db
    finally:
        client.close()  # Close the connection to the MongoDB database


def test_get_method_executes_without_error(db_session, crud_author):
    db_session.query = MagicMock(return_value=_QueryMock())
    try:
        authors = crud_author.get(db_session)
    except SQLAlchemyError as e:
        pytest.fail(f"Unexpected SQLAlchemyError occurred: {e}")
    assert (
        authors is not None
    ), "The `get` method should return a result, even if it's an empty list"
