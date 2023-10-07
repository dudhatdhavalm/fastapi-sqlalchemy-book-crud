from app.crud.book import CRUDBook
from app.crud.crud_book import *
from typing import Dict

import pytest
from app.schemas.book import BookCreate
from sqlalchemy.orm import Session
from app.models.book import Book


@pytest.fixture
def db_session() -> Session:
    # Here you should set-up and tear-down your database session.
    # I will use a context manager for the sake of simplicity.
    with Session() as session:
        yield session


@pytest.fixture
def test_book_data() -> Dict:
    return {"title": "Test book title", "pages": 300, "author_id": 1}


@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook()


def test_create(db_session: Session, test_book_data: Dict, crud_book: CRUDBook):
    book_create = BookCreate(**test_book_data)
    new_book = crud_book.create(db_session, obj_in=book_create)

    assert new_book.title == test_book_data["title"]
    assert new_book.pages == test_book_data["pages"]
    assert new_book.author_id == test_book_data["author_id"]
    assert isinstance(new_book.created_at, date)
