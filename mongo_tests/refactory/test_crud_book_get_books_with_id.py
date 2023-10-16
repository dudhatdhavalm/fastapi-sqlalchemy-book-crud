import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from app.crud.crud_book import CRUDBook
from app.crud.crud_book import *
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection



@pytest.fixture
def db_session() -> MongoClient:
    return MongoClient("mongodb://localhost:27017/BooksDB")


def test_get_books_with_id_no_errors(crud_book: CRUDBook, db: MongoClient):
    result = crud_book.get_books_with_id(db, 1)
    assert result is not None


def test_get_books_with_id_nonexistent_id(crud_book: CRUDBook, mongo_session: MongoClient):
    result = crud_book.get_books_with_id(mongo_session, -1)
    assert result is None


def test_get_books_with_id_invalid_id(crud_book: CRUDBook, db_instance: Database):
    with pytest.raises(TypeError):
        crud_book.get_books_with_id(db_instance, 'abc')




@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook()

@pytest.fixture
def db() -> Database:
    client = MongoClient('localhost', 27017)
    return client['mydatabase']
