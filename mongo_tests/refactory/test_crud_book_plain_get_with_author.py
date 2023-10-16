from app.crud.crud_book_plain import *
from sqlalchemy import create_engine
from app.models.author import Author
from sqlalchemy.orm import sessionmaker
from app.models.book import Book
from datetime import date

import pytest
from sqlalchemy.pool import StaticPool
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


@pytest.fixture(scope="module")
def db():
    """
    Create a new database session for a test
    """
    client = MongoClient("mongodb://localhost:27017") 
    # database name, user name and password will depend on Mongo configurations.
    db = client.BooksDB

    yield db

    client.close()


def test_get_books_with_author_empty(db):
    """
    Test to verify the functionality of 'get_with_author' with no data
    """
    # when
    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    cursor = collection.find({})
    books = []
    for document in cursor:
        books.append(document)

    # then
    assert books == []


def test_get_with_author(db):
    """
    Test to verify if function 'get_with_author' is compiled
    without raising any exceptions
    """
    CRUD_books = CRUDBook()
    response = CRUD_books.get_with_author(db)
    assert response is not None


def test_get_books_with_author(db):
    """
    Test to verify the functionality of 'get_with_author' with dummy data
    """
    # given
    author = {"name": "Author1"}
    author_id = db.authors.insert_one(author).inserted_id

    book1 = {"title": "Book1", "pages": 150, "created_at": datetime.now(), "author_id": author_id}
    book2 = {"title": "Book2", "pages": 200, "created_at": datetime.now(), "author_id": author_id}
    db.books.insert_many([book1, book2])

    # when
    CRUD_books = CRUDBook()
    books = CRUD_books.get_with_author(db)

    # then
    assert db.books.count_documents({}) == 2
    assert all([isinstance(book, dict) for book in books])
