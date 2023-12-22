

from datetime import date
from app.models.book import Book

from app.crud.crud_book_plain import *
from unittest.mock import patch
from app.models.author import Author

import pytest

from app.models.author import Author
from app.crud.crud_book_plain import CRUDBook
from sqlalchemy.orm import Session


@pytest.fixture
def dummy_books():
    return [
        Book(id=1, title="Book One", pages=100, created_at=date.today(), author_id=1),
        Book(id=2, title="Book Two", pages=200, created_at=date.today(), author_id=2),
    ]


@pytest.fixture
def db_session_mock(dummy_books):
    with patch("sqlalchemy.orm.Session") as mock:
        db = mock.return_value.__enter__.return_value
        db.query.return_value.join.return_value.all.return_value = dummy_books
        yield db


def test_get_with_author_runs_without_errors(db_session_mock):
    """Test if the get_with_author function runs without errors and returns a list."""
    crud_book = CRUDBook()
    result = crud_book.get_with_author(db_session_mock)
    assert (
        result is not None
    ), "The `get_with_author` method should return a non-None result"
