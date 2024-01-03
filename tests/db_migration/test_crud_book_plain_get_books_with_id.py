
from app.crud.crud_book import CRUDBook
from sqlalchemy.orm import Session

import pytest
from app.models.book import Book


from datetime import date
from app.crud.crud_book_plain import *
from unittest.mock import MagicMock
from app.models.author import Author

# No need to set up the database URL or engine since we will mock the database calls


@pytest.fixture
def db() -> Session:
    """Fixture to create a mock database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def dummy_book(db: Session) -> Book:
    """Fixture to create a mock book without inserting it into the database."""
    book = Book(
        id=1, title="Test Book", pages=123, author_id=1, created_at=date(2020, 1, 1)
    )
    return book


@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook()


def test_get_books_with_id_does_not_throw(
    db: Session, dummy_book: Book, crud_book: CRUDBook
):
    db.query.return_value.join.return_value.filter.return_value.first.return_value = (
        dummy_book
    )
    assert crud_book.get_books_with_id(db, dummy_book.id) is not None


def test_get_books_with_id_returns_correct_book(
    db: Session, dummy_book: Book, crud_book: CRUDBook
):
    db.query.return_value.join.return_value.filter.return_value.first.return_value = (
        dummy_book
    )
    book = crud_book.get_books_with_id(db, dummy_book.id)
    assert book.id == dummy_book.id
    assert book.title == dummy_book.title
    assert book.pages == dummy_book.pages


def test_get_books_with_id_with_invalid_id(db: Session, crud_book: CRUDBook):
    db.query.return_value.join.return_value.filter.return_value.first.return_value = (
        None
    )
    invalid_id = -1
    assert crud_book.get_books_with_id(db, invalid_id) is None
