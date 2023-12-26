from app.crud.crud_book_plain import *

import pytest


from unittest.mock import create_autospec
from unittest.mock import MagicMock, create_autospec
from app.models.book import Book
from app.models.author import Author
from sqlalchemy.orm import Session
from datetime import datetime
from bson.objectid import ObjectId
from unittest.mock import MagicMock


@pytest.fixture
def mock_db_session():
    # Mock pymongo's collection methods
    mock_collection = MagicMock()

    # Prepare the mock data
    mock_books = [
        {
            '_id': ObjectId(),
            'title': "Book 1",
            'isbn_number': 123,
            'publication_date': datetime(2021, 5, 3),
            'author_id': 1,
            'author_name': "Author 1"
        },
        {
            '_id': ObjectId(),
            'title': "Book 2",
            'isbn_number': 456,
            'publication_date': datetime(2021, 6, 4),
            'author_id': 2,
            'author_name': "Author 2"
        },
    ]

    # Mock the find method to return our mock data
    mock_collection.find.return_value = mock_books

    # Mock the database to return our mock collection
    mock_db = MagicMock()
    mock_db.books = mock_collection
    
    # Normally, pymongo would return a collection object from db['books']
    # or db.books, but here we just return the mocked collection directly
    return mock_db


@pytest.fixture
def crud_book():
    return CRUDBook()


def test_get_with_author_no_errors(crud_book, mock_db_session):
    try:
        result = crud_book.get_with_author(db=mock_db_session)
        assert result is not None
    except Exception:
        pytest.fail("get_with_author method should not raise an exception.")


# You would need to mock or reference the collection from your database
# Let's assume you have a books_collection for the sake of this example

def test_get_with_author_no_results(crud_book, mocked_collection):
    # Mock the find method of the collection to return empty list
    mocked_collection.find.return_value = []
    
    # Call the method to be tested with the mocked collection
    result = crud_book.get_with_author(db=mocked_collection)
    
    # Assert that the returned result is an empty list
    assert result == []


def test_get_with_author_returns_list(crud_book, mock_db_session):
    result = crud_book.get_with_author(db=mock_db_session)
    assert isinstance(result, list)

@pytest.fixture
def mocked_collection():
    # Create a MagicMock object to simulate the pymongo collection
    collection = MagicMock()
    collection.find = MagicMock(return_value=[])
    return collection
