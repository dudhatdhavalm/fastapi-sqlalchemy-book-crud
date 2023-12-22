from datetime import date
from app.models.book import Book

from app.crud.crud_book_plain import *
from unittest.mock import patch
from app.models.author import Author

import pytest

from app.models.author import Author
from app.crud.crud_book_plain import CRUDBook
from sqlalchemy.orm import Session
from datetime import datetime
from unittest.mock import MagicMock
from pymongo.collection import Collection
from unittest.mock import patch, MagicMock


# Assuming 'dummy_books' is a list of dictionaries representing book documents

@pytest.fixture
def db_session_mock(dummy_books):
    with patch("pymongo.collection.Collection.find") as mock_find:
        mock_collection = MagicMock(spec=Collection)
        mock_find.return_value = dummy_books  # PyMongo find() method returns a cursor which can be iterated over, not a list
        mock_collection.find = mock_find
        yield mock_collection


# Required fixture for PyMongo test cases
@pytest.fixture
def dummy_books():
    return [
        {"title": "Book One", "pages": 100, "created_at": datetime.utcnow(), "author_id": 1},
        {"title": "Book Two", "pages": 200, "created_at": datetime.utcnow(), "author_id": 2},
    ]

@pytest.fixture
def mock_collection(dummy_books):
    collection = MagicMock(spec=Collection)
    # Setup your mock collection behavior here
    # For example, to mock the find() method that returns all books:
    collection.find.return_value = dummy_books
    # To mock the find_one() method that returns a single book:
    collection.find_one.side_effect = lambda query: next((book for book in dummy_books if book['author_id'] == query['author_id']), None)
    return collection


def test_get_with_author_runs_without_errors(db_session_mock):
    """Test if the get_with_author function runs without errors and returns a list."""
    crud_book = CRUDBook()
    result = crud_book.get_with_author(db_session_mock)
    assert (
        result is not None
    ), "The `get_with_author` method should return a non-None result"
