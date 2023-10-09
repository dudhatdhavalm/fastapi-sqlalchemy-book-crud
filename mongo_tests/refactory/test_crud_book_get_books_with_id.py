from sqlalchemy import create_engine
import pytest
from app.crud.crud_book import *
from sqlalchemy.orm import Session, sessionmaker
from app.models.author import Author


from datetime import date

import pytest
from app.models.book import Book
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


# Create a database connection for the tests
@pytest.fixture(scope="module")
def test_db():
    client = MongoClient('localhost', 27017)
    db = client['BooksDB']

    # Create collections if they don't exist
    if 'books' not in db.list_collection_names():
        db.create_collection('books')

    if 'authors' not in db.list_collection_names():
        db.create_collection('authors')
        
    return db


def test_get_books_with_id_non_existing(test_db: MongoClient, test_crud_book: CRUDBook):
    # Given - No data in db

    # When
    result = test_crud_book.get_books_with_id(test_db, 99)

    # Then
    assert result is None


# Test case for existing book id
def test_get_books_with_id_existing(test_db: MongoClient, test_crud_book: CRUDBook):
    # Given
    book1 = {
        "_id": ObjectId(),
        "title": "Book1",
        "pages": 100,
        "created_at": datetime(2020, 5, 17), 
        "author_id": ObjectId()
    }
    
    author1 = {
        "_id": ObjectId(),
        "name": "Author1"
    }
    
    test_db.books.insert_one(book1)
    test_db.authors.insert_one(author1)
    
    # When
    result = test_db.books.find_one({"_id": book1["_id"]})

    # Then
    assert result["_id"] == book1["_id"]
    assert result["title"] == "Book1"



# Create a test object of CRUDBook
@pytest.fixture(scope="module")
def test_crud_book():
    client = MongoClient()
    db = client.test_database
    return CRUDBook(db)
