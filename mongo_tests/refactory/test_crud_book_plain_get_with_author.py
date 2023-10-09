import pytest

from sqlalchemy import create_engine
from app.models.author import Author


from datetime import date
from sqlalchemy.orm import Session
from app.crud.crud_book_plain import *
from app.models.book import Book
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


def test_get_with_author(session, test_data):
    client = MongoClient('localhost', 27017)
    db = client['test-db']
    crudbook = db.crudBook  # assuming collection name is 'crudBook'
    books = crudbook.find({})
    
    # check returned books have correct format
    for book in books:
        assert isinstance(book["_id"], int)
        assert isinstance(book["title"], str)
        assert isinstance(book["pages"], int)
        assert isinstance(book["created_at"], int)  # MongoDB doesn't support date object. Usually timestamps(int) are used instead
        assert isinstance(book["author_id"], int)
        assert isinstance(book["author_name"], str)
    # check returned books include test data
    assert any(book["_id"] == test_data["book"].id for book in books)
    assert any(book["author_name"] == test_data["author"].name for book in books)


# fixture to setup and teardown a session
@pytest.fixture
def session():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["BooksDB"]
    yield db
    # teardown
    client.close()



@pytest.fixture
def test_data():
    # setup mongo client
    mongodb_uri = "your_mongodb_uri"
    client = MongoClient(mongodb_uri)
    db = client['your_database_name']
    
    # setup
    author1 = {'_id': ObjectId(), 'name': 'Author1'}
    db['author'].insert_one(author1)
    book1 = {'_id': ObjectId(), 'title': 'Book1', 'pages': 100, 'created_at': datetime.utcnow(), 'author_id': author1['_id']}
    db['book'].insert_one(book1)
    # yield data for test to use
    yield {'author': author1, 'book': book1}
    
    # teardown
    db['book'].delete_many({})
    db['author'].delete_many({})
