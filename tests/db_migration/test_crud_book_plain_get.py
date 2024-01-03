from unittest.mock import Mock
from sqlalchemy.orm import Session

import pytest
from app.models.book import Book
from app.crud.crud_book_plain import CRUDBook

from app.crud.crud_book_plain import *

# Assuming that CRUDBook is located in app/crud/crud_book_plain.py based on the file path given


@pytest.fixture
def mock_db_session():
    # Create a mock session to use in tests
    session = Mock(spec=Session)
    # Mock the query chain methods
    session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        []
    )
    return session


@pytest.fixture
def crud_book():
    return CRUDBook()


def test_get_without_errors(mock_db_session, crud_book):
    assert crud_book.get(mock_db_session) is not None


def test_get_with_skip_parameter(mock_db_session, crud_book):
    assert crud_book.get(mock_db_session, skip=10) is not None


def test_get_with_limit_parameter(mock_db_session, crud_book):
    assert crud_book.get(mock_db_session, limit=5) is not None


def test_get_with_skip_and_limit_parameters(mock_db_session, crud_book):
    assert crud_book.get(mock_db_session, skip=5, limit=5) is not None


# Required imports for the test cases above,
# placed at the bottom so they can be parsed correctly.
from unittest.mock import Mock
