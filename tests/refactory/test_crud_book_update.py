from sqlalchemy.orm import Session
from app.db.base_class import Base
from sqlalchemy.orm.session import Session
from app.models.book import Book
from datetime import date


from app.crud.book import CRUDBook
from app.crud.crud_book import *

import pytest
from typing import Any, Dict, Union


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
def book_update() -> Dict[str, Any]:
    """Create book update dictionary."""
    return {
        "title": "Updated Test book",
        "description": "Updated Test description",
    }


@pytest.fixture
def session() -> Session:
    """Create sample session."""
    return Session()


@pytest.fixture
def crud_book() -> CRUDBook:
    """Create CRUDBook instance."""
    return CRUDBook()


def test_update_no_errors(
    crud_book: CRUDBook,
    session: Session,
    sample_book: Dict[str, Any],
    book_update: Dict[str, Any],
) -> None:
    book = Book(**sample_book)
    updated_book = crud_book.update(db=session, db_obj=book, obj_in=book_update)
    assert updated_book is not None


def test_update_correct_values(
    crud_book: CRUDBook,
    session: Session,
    sample_book: Dict[str, Any],
    book_update: Dict[str, Any],
) -> None:
    book = Book(**sample_book)
    updated_book = crud_book.update(db=session, db_obj=book, obj_in=book_update)
    assert updated_book.title == book_update["title"]
    assert updated_book.description == book_update["description"]
    assert updated_book.created_at == date.today()
