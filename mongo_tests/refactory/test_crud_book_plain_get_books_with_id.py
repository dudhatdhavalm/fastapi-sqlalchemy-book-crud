from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import Session, sessionmaker
from app.models.author import Author


from datetime import date

import pytest
from app.crud.crud_book_plain import *
from app.models.book import Book
from pymongo import MongoClient
from bson import ObjectId
from bson.objectid import ObjectId
from datetime import datetime


# Test case for non-existing book id
def test_get_books_with_id_non_existing(test_db: MongoClient, test_crud_book: CRUDBook):
    # Given - No data in db

    # When
    result = test_crud_book.get_books_with_id(test_db, ObjectId(99))

    # Then
    assert result is None


# Create a database connection for the tests
@pytest.fixture(scope="module")
def test_db():
    # Creating a MongoClient instance and connect to the database.
    client = MongoClient("mongodb://localhost:27017/")
    
    # Creating and initializing our database and collections instead of tables.
    db = client["BooksDB"]
    books = db["books"]
    authors = db["authors"]
    
    # Your pytest will insert data to this database and will use it for testing.
    
    return db


# Test case for existing book id
def test_get_books_with_id_existing(test_db: MongoClient, test_crud_book: CRUDBook):
    # Given
    book1 = Book(
        id=ObjectId(), title="Book1", pages=100, created_at=datetime(2020, 5, 17), author_id=ObjectId()
    )
    author1 = Author(id=ObjectId(), name="Author1")
    test_db.testdb.author1.insert_one(vars(author1))
    test_db.testdb.book1.insert_one(vars(book1))

    # When
    result = test_crud_book.get_books_with_id(test_db, book1.id)

    # Then
    assert result["_id"] == book1.id
    assert result["title"] == "Book1"


# Create a test object of CRUDBook
@pytest.fixture(scope="module")
def test_crud_book():
    client = MongoClient('localhost', 27017)
    my_db = client.my_database
    return my_db['books']
