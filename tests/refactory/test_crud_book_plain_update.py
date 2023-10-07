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
    db: Session,
    crud_book: CRUDBook,
    test_book: Dict[str, Any],
    test_book_updated: Dict[str, Any],
):
    # Create a test book
    created_book = Book(**test_book)
    db.add(created_book)
    db.commit()

    # Make sure the book is created with the correct data
    assert created_book.title == test_book["title"]
    assert created_book.description == test_book["description"]
    assert str(created_book.publication_date) == test_book["publication_date"]
    assert created_book.author_id == test_book["author_id"]

    # Update the book and assert the book data is updated successfully
    updated_book = crud_book.update(db, db_obj=created_book, obj_in=test_book_updated)
    assert updated_book.title == test_book_updated["title"]
    assert updated_book.description == test_book_updated["description"]
    assert str(updated_book.publication_date) == test_book_updated["publication_date"]
    assert updated_book.author_id == test_book_updated["author_id"]
    assert updated_book.created_at == date.today()

    # Test with book instance
    another_book = Book(**test_book)
    db.add(another_book)
    db.commit()
    updated_book = crud_book.update(db, db_obj=another_book, obj_in=another_book)
    assert updated_book.title == test_book["title"]
    assert updated_book.description == test_book["description"]
    assert str(updated_book.publication_date) == test_book["publication_date"]
    assert updated_book.author_id == test_book["author_id"]
    assert updated_book.created_at == date.today()
