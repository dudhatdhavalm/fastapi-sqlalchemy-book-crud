from sqlalchemy.orm import Session

import pytest
from app.schemas.book import BookCreate
from app.db.session import SessionLocal
from app.crud.crud_book import *
from typing import Any, Dict, List, TypeVar, Union
from app.crud.crud_book import CRUDBook
from datetime import date
from app.crud.base import CRUDBase


@pytest.fixture(scope="module")
def test_db() -> Session:
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="module")
def new_book() -> BookCreate:
    return BookCreate(title="Test book", pages=200, author_id=1)


def test_create(test_db: Session, new_book: BookCreate):
    """Test the create function"""
    # Instantiate the CRUDBook with the Book model
    from app.models.book import Book

    book_operations = CRUDBook(Book)

    # Use the create method
    result = book_operations.create(test_db, obj_in=new_book)

    # Validate that the function executed without error and a result is present
    assert result is not None, "The create function did not return a result"
