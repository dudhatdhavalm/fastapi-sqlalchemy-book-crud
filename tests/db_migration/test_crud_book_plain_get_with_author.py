
import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from app.crud.crud_book_plain import *


@pytest.fixture
def db_session():
    # Create a mock session object
    mock_session = MagicMock(spec=Session)

    # Setup the query method to return an iterable that resembles the query result
    mock_query_result = [
        MagicMock(
            id=1,
            title="Book One",
            pages=100,
            created_at=date(2021, 5, 21),
            author_id=1,
            author_name="Author One",
        ),
        MagicMock(
            id=2,
            title="Book Two",
            pages=200,
            created_at=date(2021, 6, 21),
            author_id=2,
            author_name="Author Two",
        ),
    ]
    # We have to use side_effect to be able to call all()
    mock_session.query().join().all.side_effect = [mock_query_result]

    return mock_session


def test_get_with_author_no_errors(db_session):
    crud_book = CRUDBook()
    result = crud_book.get_with_author(db_session)
    assert result is not None, "The function should return a value."


def test_get_with_author_correct_mapping(db_session):
    crud_book = CRUDBook()
    books_with_authors = crud_book.get_with_author(db_session)
    assert (
        len(books_with_authors) == 2
    ), "There should be two books with authors in the result."
    assert (
        books_with_authors[0].author_name == "Author One"
    ), "The author name should be correctly mapped in the result."


def test_get_with_author_author_id(db_session):
    crud_book = CRUDBook()
    books_with_authors = crud_book.get_with_author(db_session)
    assert (
        books_with_authors[0].author_id == 1
    ), "The author ID should be correctly mapped in the result."


# Necessary imports
from datetime import date
