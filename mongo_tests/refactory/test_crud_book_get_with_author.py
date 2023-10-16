from sqlalchemy import create_engine
from app.models.author import Author
from sqlalchemy.orm import sessionmaker
from app.models.book import Book
from datetime import date
from app.crud.crud_book import *

import pytest
from sqlalchemy.pool import StaticPool
from pymongo import MongoClient
import os 
from bson.objectid import ObjectId
import datetime


def test_get_books_with_author_empty(db):
    """
    Test to verify the functionality of 'get_with_author' with no data
    """
    # when
    CRUD_books = CRUDBook()
    books = CRUD_books.get_with_author(db)

    # then
    assert books.count() == 0


def test_get_books_with_author(mongodb):
    """
    Test to verify the functionality of 'get_with_author' with dummy data
    """
    # given
    author_id = mongodb.authors.insert_one({"name": "Author1"}).inserted_id

    book1 = {"title": "Book1", "pages": 150, "created_at": datetime.datetime.utcnow(), "author_id": author_id}
    book2 = {"title": "Book2", "pages": 200, "created_at": datetime.datetime.utcnow(), "author_id": author_id}
    mongodb.books.insert_many([book1, book2])

    # when
    books = list(mongodb.books.find({"author_id": author_id}))

    # then
    assert len(books) == 2
    assert all([isinstance(book, dict) for book in books])


def test_get_with_author(db):
    """
    Test to verify if function 'get_with_author' is compiled
    without raising any exceptions
    """
    CRUD_books = CRUDBook()
    response = CRUD_books.get_with_author(db)
    assert response is not None


@pytest.fixture(scope='module')
def db():
    """
    Create a new database session for a test
    """
    connection = MongoClient(
        "DB_URL_HERE",
        username='USERNAME_HERE',
        password='PASSWORD_HERE',
    )

    db = connection['Database_Name']

    yield db

    connection.close()
