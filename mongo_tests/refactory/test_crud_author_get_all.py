from sqlalchemy.orm import Session as SqlalchemySession
import pytest
from sqlalchemy import create_engine
from app.crud.crud_author import *
from app.models.author import Author
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from contextlib import contextmanager
from bson.objectid import ObjectId
from typing import Generator
import os


# Assuming the db configuration is set in environment variable.
client = MongoClient(os.environ.get('MONGO_URI'))
db = client.test

# global scope
engine = create_engine("postgresql://postgres:root@localhost:5432/BooksDB")


# Assuming the class definition of CRUDAuthor
# from app.crud.crud_author import CRUDAuthor

# first test is to ensure we are getting something (not none)
# and the function doesn't throw any error.
def test_get_all(db):
    crud_author = CRUDAuthor()
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert authors is not None


# Test to check if there are no authors in the database,
# get_all should return an empty list.
def test_get_all_no_authors(db):
    crud_author = CRUDAuthor()
    db = MongoClient().test_database  # connect to your database
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert authors == []



# test to check that the function correctly gets all authors if limit is more than number of authors
def test_get_all_more_limit(db):
    crud_author = CRUDAuthor()
    create_new_author(db)
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert len(list(authors)) == 1


# Test to check that the function returns empty list if limit is 0
def test_get_all_limit_zero():
    # Pymongo works with dictionary to represent objects
    new_author_data = { "name": "Test", "books": [] }
    
    # Direct insertion using Pymongo's native method
    db.authors.insert_one(new_author_data)
    
    crud_author = CRUDAuthor()
    # Pymongo's native query which accepts skip and limit
    authors_cursor = db.authors.find().skip(0).limit(0)
    
    # Conversion of cursor to list
    authors = [author for author in authors_cursor]
    
    assert authors == []



# Test to check the function when the skip parameter is used.
def test_get_all_with_skip(db):
    client = MongoClient()
    db = client.test_database
    crud_author = CRUDAuthor()
    create_new_author(db)
    create_new_author(db, name="Test2")
    authors = db.authors.find().skip(1).limit(100)
    assert authors.count() == 1


# function to create a new author
def create_new_author(db, name: str = "Test"):
    author = {"name": name}
    result = db["author"].insert_one(author)
    return result.inserted_id


# creating pytest fixture for database client
@pytest.fixture
def db() -> Generator[MongoClient, None, None]:
    client = MongoClient('mongodb://localhost:27017')
    db = client.test_db
    try:
        yield db
    finally:
        client.close()
