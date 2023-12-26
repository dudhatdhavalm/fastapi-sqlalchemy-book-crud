
from app.crud.crud_book_plain import *

import pytest


from unittest.mock import create_autospec
from unittest.mock import MagicMock, create_autospec
from app.models.book import Book
from app.models.author import Author
from sqlalchemy.orm import Session


# Fixture for the mocked session
@pytest.fixture
def mock_db_session():
    # Create an autospec of the Session class
    mock_session = create_autospec(Session, instance=True)

    # Mock the query chain to return a mock
    mock_query = mock_session.query.return_value.join.return_value.all

    # Mock the return value of the query results
    mock_books = [
        (1, "Book 1", 123, date(2021, 5, 3), 1, "Author 1"),
        (2, "Book 2", 456, date(2021, 6, 4), 2, "Author 2"),
    ]
    mock_query.return_value = mock_books

    return mock_session


# Fixture for the CRUDBook instance
@pytest.fixture
def crud_book():
    return CRUDBook()


# Test that no errors are thrown when the function is executed
def test_get_with_author_no_errors(crud_book, mock_db_session):
    try:
        result = crud_book.get_with_author(db=mock_db_session)
        assert result is not None
    except Exception:
        pytest.fail("get_with_author method should not raise an exception.")


# Test that the function returns a list when a session is passed
def test_get_with_author_returns_list(crud_book, mock_db_session):
    result = crud_book.get_with_author(db=mock_db_session)
    assert isinstance(result, list)


# Test the edge case when the database session returns no results
def test_get_with_author_no_results(crud_book, mock_db_session):
    mock_db_session.query.return_value.join.return_value.all.return_value = []
    result = crud_book.get_with_author(db=mock_db_session)
    assert result == []
