from sqlalchemy.orm import Session

import pytest
from app.schemas.book import BookCreate
from app.db.session import SessionLocal
from app.crud.crud_book import *
from typing import Any, Dict, List, TypeVar, Union
from app.crud.crud_book import CRUDBook
from datetime import date
from app.crud.base import CRUDBase
from pymongo import MongoClient
from pytest import fixture
from bson.objectid import ObjectId


def test_create(client: MongoClient, new_book: Dict[str, Any]):
    """Test the create function"""
    from app.models.book import Book

    # Connect to the mongodb database
    db = client.test_db

    # Get the 'books' collection
    books = db.books

    # Use pymongo's insert_one function to add a new book to the collection
    result = books.insert_one(new_book)

    # Use assert to check that the insertion was successful
    assert result.inserted_id is not None, "The create function did not return a result"


@pytest.fixture(scope="module")
def new_book() -> Dict:
    return {"title": "Test book", "pages": 200, "author_id": ObjectId()}


@fixture(scope="module")
def test_db() -> MongoClient:
    client = MongoClient('mongodb://localhost:27017/')  # use your MongoDB connection string here
    db = client.your_db_name  # specify your database name
    yield db
    client.close()
