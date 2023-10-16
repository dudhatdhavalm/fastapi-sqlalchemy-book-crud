from sqlalchemy.orm import Session
from app.db.base_class import Base
from sqlalchemy.orm.session import Session
from app.models.book import Book
from datetime import date


from app.crud.book import CRUDBook
from app.crud.crud_book import *

import pytest
from typing import Any, Dict, Union
from typing import Any, Dict
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime


@pytest.fixture
def sample_book() -> Dict[str, Any]:
    """Create sample book dictionary."""
    return {
        "title": "Test book",
        "description": "Test description",
        "isbn": "978-3-16-148410-0",
        "author_id": 1,
        "publication_date": date.today(),
    }


@pytest.fixture
def session() -> MongoClient:
    """Create sample session."""
    return MongoClient('mongodb://localhost:27017/')


@pytest.fixture
def crud_book() -> CRUDBook:
    """Create CRUDBook instance."""
    return CRUDBook()



def test_update_correct_values(
    client: MongoClient,
    sample_book: Dict[str, Any],
    book_update: Dict[str, Any],
) -> None:
    db = client.test_database
    books = db.books
    result = books.insert_one(sample_book)
    book_id = result.inserted_id

    updated_book = books.find_one_and_update(
        {"_id": book_id}, 
        {"$set": book_update}, 
        return_document=True
    )
   
    assert updated_book["title"] == book_update["title"]
    assert updated_book["description"] == book_update["description"]
    assert updated_book["created_at"].date() == datetime.today().date()



def test_update_no_errors(
    mongo_db: MongoClient,
    sample_book: Dict[str, Any],
    book_update: Dict[str, Any],
) -> None:
    book = Book(**sample_book)
    book_id = mongo_db.Books.insert_one(book).inserted_id
    updated_book = mongo_db.Books.find_one_and_update({"_id": ObjectId(book_id)}, {"$set": book_update}, return_document=True)
    assert updated_book is not None


@pytest.fixture
def book_update() -> Dict[str, Any]:
    """Create book update dictionary."""
    return {
        "title": "Updated Test book",
        "description": "Updated Test description",
    }
