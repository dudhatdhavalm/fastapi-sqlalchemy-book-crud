from app.crud.crud_book_plain import *
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from app.crud.crud_book import CRUDBook
from pymongo import MongoClient

# Initializing a pymongo client
client = MongoClient()

# Getting handle to the test database
db = client.test_database


def test_get_books_with_id_no_errors(crud_book: CRUDBook, client: MongoClient):
    result = crud_book.get_books_with_id(client, 1)
    assert result is not None


def test_get_books_with_id_nonexistent_id(crud_book: CRUDBook, db):
    result = crud_book.get_books_with_id(db, -1)
    assert result is None


def test_get_books_with_id_invalid_id(crud_book: CRUDBook, db_session: MongoClient):
    with pytest.raises(TypeError):
        crud_book.get_books_with_id(db_session, "abc")

# Getting handle to the books collection
collection = db.books


@pytest.fixture
def db_session():
    client = MongoClient("mongodb://localhost:27017")
    return client['BooksDB']


@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook(collection)
