from datetime import date
from app.models.book import Book

from app.crud.crud_book_plain import *
from app.models.author import Author

import pytest
from unittest.mock import MagicMock
from datetime import date
from app.crud.crud_book_plain import CRUDBook
from sqlalchemy.orm import Session

from typing import List, Tuple
from pymongo.collection import Collection
from app.crud.crud_book import CRUDBook  # Assumed location of the CRUDBook class for MongoDB
from pymongo import MongoClient


# Assuming CRUDBook is already adapted for MongoDB operations

@pytest.fixture
def crud_book():
    return CRUDBook()


# The test case function name stays the same
def test_get_with_author_no_errors(crud_book, db_session_mock):
    try:
        # Call the function to get books with authors
        # Note: In PyMongo, db_session_mock would be representative of a connection or a collection, not an ORM session
        crud_book.get_with_author(db_session_mock)
    except Exception as e:
        pytest.fail(f"An error occurred: {e}")


@pytest.fixture
def db_session_mock():
    db_session = MagicMock(spec=Session)
    return db_session

@pytest.fixture
def mongo_client_mock():
    # This should be a mock or MagicMock object representing a MongoClient
    client = MagicMock(spec=MongoClient)
    client["testdb"]["testcollection"] = mongo_collection_mock()  # Link the test collection mock
    return client

@pytest.fixture
def mongo_collection_mock(mocker):
    # Using pytest-mock plugin to create a mock of the MongoDB collection
    return mocker.patch.object(CRUDBook, 'collection', new_callable=lambda: mocker.MagicMock(spec=Collection))


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


def test_get_with_author_with_data(crud_book, db_session_mock, db_data):
    db_session_mock.query().join().all.return_value = db_data

    books_with_authors = crud_book.get_with_author(db_session_mock)

    assert books_with_authors is not None
    assert isinstance(books_with_authors, list)
    assert all(isinstance(book, tuple) for book in books_with_authors)


def test_get_with_author_no_data(crud_book, db_session_mock):
    db_session_mock.query().join().all.return_value = []

    books_with_authors = crud_book.get_with_author(db_session_mock)

    assert books_with_authors == []
