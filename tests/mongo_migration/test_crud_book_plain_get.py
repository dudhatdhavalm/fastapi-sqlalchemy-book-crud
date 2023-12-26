from app.crud.crud_book_plain import *

import pytest
from unittest.mock import MagicMock


from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from pymongo.collection import Collection
import pymongo



@pytest.fixture
def db_session():
    session = MagicMock(spec=Session)

    session.query().offset().limit().all.return_value = []

    return session


@pytest.fixture
def crud_book():
    return CRUDBook()


# Defining fixtures for pymongo testing
@pytest.fixture
def skip():
    return 0


@pytest.fixture
def limit():
    return 100


# Note that in PyMongo context, db_session may refer to the collection object instead
def test_get_returns_list(crud_book, collection, skip, limit):
    result = crud_book.get(collection, skip=skip, limit=limit)
    assert isinstance(result, list), "The 'get' function should return a list"


# Assuming that 'crud_book' is a class that handles the MongoDB operations
# and has a 'get' method similar to the SQLAlchemy version.

def test_get_custom_skip_limit(crud_book):
    custom_skip = 10
    custom_limit = 50
    mock_collection = MagicMock()

    # Setup the mock_collection to return a mongo cursor-like object for chaining.
    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor  # Return itself for chaining
    mock_cursor.limit.return_value = mock_cursor  # Return itself for chaining
    mock_collection.find.return_value = mock_cursor

    # Replace db_session (SQLAlchemy session) with the mock_collection (MongoDB collection)
    result = crud_book.get(mock_collection, skip=custom_skip, limit=custom_limit)

    # Check that skip and limit were called with proper values
    mock_cursor.skip.assert_called_with(custom_skip)
    mock_cursor.limit.assert_called_with(custom_limit)

    assert result is not None, "The 'get' function returned None with custom skip and limit"


def test_get_with_default_params(crud_book, db_session):
    # Assuming db_session is a MagicMock representing a pymongo collection
    db_session.find.return_value = db_session  # Enable method chaining for this mock
    db_session.skip.return_value = db_session  # Enable method chaining for the skip mock
    db_session.limit.return_value = db_session  # Enable method chaining for the limit mock
    
    result = crud_book.get(db_session)  # Pass the mocked collection to the get method
    
    db_session.find.assert_called_with({})  # Assert find method called with no filtering
    db_session.skip.assert_called_with(0)  # Assert skip method called with default starting index
    db_session.limit.assert_called_with(100)  # Assert limit method called with default limit (page size)
    
    assert result is not None, "The 'get' function returned None with default parameters"


# Assume the following import will bring the required crud_book object
# from app.crud.crud_book_mongo import crud_book

def test_get_negative_skip(crud_book):
    # Given
    negative_skip = -10

    # MagicMock representing the pymongo collection that crud_book would be querying
    collection_mock = MagicMock()
    crud_book.collection = collection_mock

    # When
    result = crud_book.get(skip=negative_skip)

    # Then
    collection_mock.find.assert_called_once()
    
    # Ensuring skip was called with the appropriate value
    args, kwargs = collection_mock.find.call_args
    assert 'skip' in kwargs, "skip was not passed as a parameter to the find method."
    assert kwargs['skip'] == max(0, negative_skip), "The 'skip' parameter should not be negative."

    assert result is not None, "The 'get' function returned None with a negative skip value"


# Assuming that 'crud_book.get' is adapted to use PyMongo
# and the 'db_session' is a PyMongo database or collection object

def test_get_negative_limit(crud_book, db_session):
    negative_limit = -10
    db_session.find = MagicMock()
    
    result = crud_book.get(db_session, limit=negative_limit)
    
    db_session.find.assert_called_with({})
    db_session.find().limit.assert_called_with(negative_limit)
    
    assert (
        result is not None
    ), "The 'get' function returned None with a negative limit value"


# As pymongo uses a different connection setup, we'll assume we have a "db_collection" fixture
# representing the MongoDB collection instead of an "db_session" SQLAlchemy session fixture.

def test_get_no_errors(crud_book, db_collection, skip, limit):
    # In pymongo, find() is used to retrieve documents from a collection, potentially with skip and limit.
    # The find method returns a cursor, which can be converted to a list for assertion.
    result = list(crud_book.get(db_collection, skip=skip, limit=limit))
    assert result is not None, "The 'get' function returned None"
