import pytest
from app.crud.crud_book import *

from sqlalchemy import create_engine
from app.models.author import Author


from datetime import date
from sqlalchemy.orm import Session
from app.models.book import Book
from pymongo import MongoClient
import pymongo


# fixture to setup and teardown a session
@pytest.fixture
def session():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['BooksDB']
    yield db
    client.close()



# fixture to setup and teardown some test data
@pytest.fixture
def test_data():
    client = MongoClient('localhost', 27017)
    database = client['test_database']
    author_collection = database['Author']
    book_collection = database['Book']

    # setup
    author1 = {"_id": 1, "name": "Author1"}
    author_collection.insert_one(author1)
    book1 = {"_id": 1, "title": "Book1", "pages": 100, "created_at": date.today(), "author_id": 1}
    book_collection.insert_one(book1)
    yield {"author": author1, "book": book1}
    # teardown
    book_collection.delete_many({"_id": 1})
    author_collection.delete_many({"_id": 1})


def test_get_with_author(session, test_data):
    crudbook = CRUDBook()
    books = crudbook.get_with_author(session)
    # check returned books have correct format
    for book in books:
        assert isinstance(book["_id"], int)
        assert isinstance(book["title"], str)
        assert isinstance(book["pages"], int)
        assert isinstance(book["created_at"], str)  # MongoDB stores datetime as string
        assert isinstance(book["author_id"], int)
        assert isinstance(book["author_name"], str)
    # check returned books include test data
    assert any(book["_id"] == test_data["book"]._id for book in books)
    assert any(book["author_name"] == test_data["author"].name for book in books)
