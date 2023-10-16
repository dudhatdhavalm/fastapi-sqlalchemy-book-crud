import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from app.crud import CRUDBase
from app.crud.base import *
from app.models import Book


from typing import Generator
from sqlalchemy.orm import sessionmaker

from app.crud import CRUDBase
from pymongo import MongoClient
from bson.objectid import ObjectId

# Replace 'your_connection_string' with your MongoDB connection string.
client = MongoClient('your_connection_string')
db = client['test-database']
collection = db['test-collection']



# Define a fixture for the database session
@pytest.fixture(scope="module")
def db() -> Generator:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["BooksDB"]

    yield db
    client.close()


# Test to check if function doesn't throw any errors when executed
# and it returns data (the function should return a list)
def test_get_multi_no_errors(db: MongoClient):
    crud = CRUDBase(Book)
    result = crud.get_multi(db)
    assert result is not None


# Test to check for working of skip and limit parameters
def test_get_multi_skip_limit(db: MongoClient):
    crud = CRUDBase(Book)
    all_books = list(db.books.find({}))
    skipped_books = list(db.books.find({}).skip(1))
    limited_books = list(db.books.find({}).limit(1))

    # If books are present in db
    if all_books:
        assert len(skipped_books) == len(all_books) - 1
        assert len(limited_books) == 1



def test_get_multi_negative_skip_limit():
    crud = CRUDBase(collection)
    result = crud.get_multi(skip=-9999, limit=-9999)
    assert result is not None



# Test to check if providing very high skip doesn't cause errors
def test_get_multi_high_skip(db: MongoClient):
    crud = CRUDBase(Book)
    result = crud.get_multi(db, skip=9999)
    assert result is not None
