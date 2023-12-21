from unittest.mock import MagicMock

import pytest
from unittest.mock import MagicMock
from app.crud.crud_book_plain import CRUDBook

from app.crud.crud_book_plain import *
from bson import ObjectId


@pytest.fixture(scope="module")
def db_session():
    db_session_mock = MagicMock()
    db_session_mock.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        Book()
    ]
    return db_session_mock


@pytest.mark.parametrize("skip, limit", [(0, 100), (20, 10), (0, 0)])
def test_get_with_different_limits_and_offsets(mongo_collection, skip, limit):
    # mongo_collection is to be set up via a pytest fixture as a MongoDB collection ready for testing
    crud_book = CRUDBook(mongo_collection)
    result = crud_book.get(skip=skip, limit=limit)
    assert result is not None


def test_get_without_parameters(mongo_client):
    # Assuming CRUDBook has been refactored to work with PyMongo
    crud_book = CRUDBook()
    result = crud_book.get(mongo_client)
    assert result is not None

# A fixture to create a MongoDB collection for the test
@pytest.fixture
def mongo_collection(mongo_client):
    # mongo_client is a fixture provided by pytest-mongo plugin that provides a connection to a test MongoDB instance
    # Here we assume the db name is 'test_database' and the collection name is 'books'
    # Configure these names as per your requirements
    collection = mongo_client["test_database"]["books"]
    # Insert test data into the collection if necessary
    # collection.insert_many([{'_id': ObjectId(), 'title': 'Book 1'}, {'_id': ObjectId(), 'title': 'Book 2'}])
    yield collection
    # Clean up the collection after tests run
    collection.delete_many({})

from app.models.book import (  # Mock Book model that may be used within the database session mock
    Book,
)
