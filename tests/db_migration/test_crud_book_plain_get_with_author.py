from sqlalchemy.orm import Session

from app.crud.crud_book_plain import *

from app.crud.crud_book_plain import CRUDBook

import pytest


from unittest.mock import MagicMock
from app.models.book import Book
from app.crud.crud_book_plain import CRUDBook
from unittest.mock import MagicMock


# Create a fixture to mock the Session object
@pytest.fixture(scope="module")
def mock_session():
    session = MagicMock(spec=Session)
    return session


# Create CRUDBook instance pytest fixture
@pytest.fixture(scope="module")
def crud_book():
    return CRUDBook()


def test_get_with_author_no_errors(crud_book, mock_session):
    """Test get_with_author doesn't raise errors and returns not None."""
    assert crud_book.get_with_author(mock_session) is not None


def test_get_with_author_return_type(crud_book, mock_session):
    """Test get_with_author returns a list."""
    mock_session.query().join().all.return_value = []
    result = crud_book.get_with_author(mock_session)
    assert isinstance(result, list)


def test_get_with_author_result_content(crud_book, mock_session):
    """Test get_with_author returns a list of tuples with correct structure."""
    mock_return_value = [
        (1, "Book Title", 123, None, 1, "Author Name"),
    ]
    mock_session.query().join().all.return_value = mock_return_value
    expected_structure = (int, str, int, None.__class__, int, str)

    results = crud_book.get_with_author(mock_session)

    # Check if all results match the expected structure
    for result in results:
        assert isinstance(result, tuple)
        assert all(
            isinstance(field, expected_type)
            for field, expected_type in zip(result, expected_structure)
        )
