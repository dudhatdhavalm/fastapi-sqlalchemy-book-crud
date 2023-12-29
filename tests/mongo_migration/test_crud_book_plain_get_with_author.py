from sqlalchemy.orm import Session

from app.crud.crud_book_plain import *

from app.crud.crud_book_plain import CRUDBook

import pytest


from unittest.mock import MagicMock
from app.models.book import Book
from app.crud.crud_book_plain import CRUDBook
from unittest.mock import MagicMock
from app.crud.crud_book import CRUDBook
from bson.objectid import ObjectId


@pytest.fixture(scope="module")
def mock_session():
    session = MagicMock(spec=Session)
    return session


@pytest.fixture(scope="module")
def crud_book():
    return CRUDBook()


def test_get_with_author_no_errors(crud_book, mock_session):
    """Test get_with_author doesn't raise errors and returns not None."""
    assert crud_book.get_with_author(mock_session) is not None


# Don't import the CRUDBook class, as it's assumed to already be in the scope along with the fixtures.

def test_get_with_author_result_content(crud_book, mock_collection):
    """Test get_with_author returns a list of dicts with correct structure in MongoDB."""
    # Assuming mock_return_value is the result of a 'join' represented in MongoDB documents
    mock_return_value = [
        {'_id': 1, 'title': "Book Title", 'page_count': 123, 'genre': None, 'author_id': 1, 'author_name': "Author Name"},
    ]

    # Assume CRUDBook.get_with_author has been adapted for pymongo to retrieve documents
    # instead of SQLAlchemy tuples and mock_collection simulates a MongoDB collection
    mock_collection.aggregate.return_value = mock_return_value
    expected_structure = {'_id': int, 'title': str, 'page_count': int, 'genre': type(None), 'author_id': int, 'author_name': str}

    # Calling the method under test
    results = crud_book.get_with_author(mock_collection)

    for result in results:
        assert isinstance(result, dict)
        # Checking if each field in result matches the type in the expected_structure
        for field, expected_type in expected_structure.items():
            assert field in result, f"{field} is not present in the result"
            assert isinstance(result[field], expected_type), f"{field} does not match the expected type {expected_type}"


# Assuming the existence of a CRUDBook class compatible with pymongo

def test_get_with_author_return_type(crud_book, mock_collection):
    """Test get_with_author returns a list."""
    # In pymongo, you might use find instead of query().join().all()
    # Let's mock the find method to return an empty cursor, which acts like an empty list.
    mock_collection.find.return_value = []

    # We assume here that get_with_author now works with pymongo's collection
    result = crud_book.get_with_author(mock_collection)
    
    # In pymongo, the result from find() is a cursor, which we need to convert to a list
    assert isinstance(result, list)
