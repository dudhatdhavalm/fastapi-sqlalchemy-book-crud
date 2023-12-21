

from datetime import date
from app.models.book import Book

from app.crud.crud_book_plain import *
from app.models.author import Author

import pytest
from unittest.mock import MagicMock
from datetime import date
from app.crud.crud_book_plain import CRUDBook
from sqlalchemy.orm import Session


# Define a fixture for the CRUDBook instance.
@pytest.fixture
def crud_book():
    return CRUDBook()


# Mock the database session
@pytest.fixture
def db_session_mock():
    db_session = MagicMock(spec=Session)
    return db_session


# Fixture to simulate books and authors from database
@pytest.fixture
def db_data():
    Author_1 = Author(id=1, name="Author 1")
    Author_2 = Author(id=2, name="Author 2")

    Book_1 = Book(id=1, title="Book 1", pages=100, created_at=date.today(), author_id=1)
    Book_2 = Book(id=2, title="Book 2", pages=200, created_at=date.today(), author_id=2)

    return [
        (
            Book_1.id,
            Book_1.title,
            Book_1.pages,
            Book_1.created_at,
            Book_1.author_id,
            Author_1.name,
        ),
        (
            Book_2.id,
            Book_2.title,
            Book_2.pages,
            Book_2.created_at,
            Book_2.author_id,
            Author_2.name,
        ),
    ]


# Test the function does not raise an error
def test_get_with_author_no_errors(crud_book, db_session_mock):
    try:
        crud_book.get_with_author(db_session_mock)
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")


# Test get_with_author with database records
def test_get_with_author_with_data(crud_book, db_session_mock, db_data):
    db_session_mock.query().join().all.return_value = db_data

    books_with_authors = crud_book.get_with_author(db_session_mock)

    assert books_with_authors is not None
    assert isinstance(books_with_authors, list)
    assert all(isinstance(book, tuple) for book in books_with_authors)


# Test get_with_author when there are no books
def test_get_with_author_no_data(crud_book, db_session_mock):
    db_session_mock.query().join().all.return_value = []

    books_with_authors = crud_book.get_with_author(db_session_mock)

    assert books_with_authors == []

# Necessary imports for the test module
from typing import List, Tuple
