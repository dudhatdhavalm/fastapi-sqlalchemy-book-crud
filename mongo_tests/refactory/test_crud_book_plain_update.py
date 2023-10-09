from datetime import date
from typing import Any, Dict, Union

from app.models.book import Book


from datetime import date

import pytest
from app.schemas.book import BookCreate
from sqlalchemy.orm import Session
from typing import Any, Dict
from app.crud.crud_book_plain import *
from app.models.book import Book
import pymongo
from datetime import datetime


@pytest.fixture(scope="module")
def test_book() -> Dict[str, Any]:
    return {
        "title": "Test Book",
        "description": "Test Description",
        "publication_date": "2022-01-01",
        "author_id": 1,
    }


@pytest.fixture(scope="module")
def test_book_updated() -> Dict[str, Any]:
    return {
        "title": "Test Book Updated",
        "description": "Test Description Updated",
        "publication_date": "2022-02-01",
        "author_id": 2,
    }


def test_update_book(
    db: pymongo.database.Database,
    test_book: Dict[str, Any],
    test_book_updated: Dict[str, Any],
):
    # Create a test book
    created_book = db.books.insert_one(test_book)

    # Make sure the book is created with the correct data
    assert created_book.inserted_id is not None
    found_book = db.books.find_one({"_id": created_book.inserted_id})
    assert found_book['title'] == test_book["title"]
    assert found_book['description'] == test_book["description"]
    assert found_book['publication_date'] == test_book["publication_date"]
    assert found_book['author_id'] == test_book["author_id"]

    # Update the book and assert the book data is updated successfully
    updated_book = db.books.find_one_and_update(
        {"_id": created_book.inserted_id}, 
        {"$set": test_book_updated}, 
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert updated_book['title'] == test_book_updated["title"]
    assert updated_book['description'] == test_book_updated["description"]
    assert updated_book['publication_date'] == test_book_updated["publication_date"]
    assert updated_book['author_id'] == test_book_updated["author_id"]
    assert updated_book['created_at'].date() == datetime.utcnow().date()

    # Test with book instance
    another_book_id = db.books.insert_one(test_book).inserted_id
    found_another_book = db.books.find_one({"_id": another_book_id})
    updated_book = db.books.find_one_and_update(
        {"_id": another_book_id}, 
        {"$set": found_another_book}, 
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert updated_book['title'] == test_book["title"]
    assert updated_book['description'] == test_book["description"]
    assert updated_book['publication_date'] == test_book["publication_date"]
    assert updated_book['author_id'] == test_book["author_id"]
    assert updated_book['created_at'].date() == datetime.utcnow().date()
