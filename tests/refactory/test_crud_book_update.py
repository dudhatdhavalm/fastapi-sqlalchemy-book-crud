from app.crud.crud_book import *
from datetime import date
from fastapi import HTTPException

import pytest
from sqlalchemy.orm import Session


from typing import Any, Dict
from app.models.book import Book


@pytest.fixture
def book() -> Dict[str, Any]:
    return {
        "id": 1,
        "title": "Test Book",
        "pages": 100,
        "description": "Test Book description",
        "created_at": date.today(),
    }


@pytest.fixture
def author() -> Dict[str, Any]:
    return {"id": 1, "name": "Test Author"}


@pytest.fixture
def test_book_create() -> Dict[str, Any]:
    return {
        "title": "Test Book",
        "pages": 100,
        "description": "Test Book description",
        "author_id": 1,
    }


@pytest.fixture
def db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_update_book(
    crud: CRUDBook, db: Session, book: Book, test_book_create: Dict[str, Any]
):
    to_update = crud.get(db, book.id)

    if to_update is None:
        pytest.fail("Precondition failed, no book with id 1 found")

    new_book = crud.update(db, db_obj=to_update, obj_in=test_book_create)

    assert new_book.id == to_update.id
    assert new_book.title == test_book_create["title"]
    assert new_book.pages == test_book_create["pages"]
    assert new_book.description == test_book_create["description"]
    assert new_book.author_id == test_book_create["author_id"]
    assert new_book.created_at == to_update.created_at


def test_update_book_failure(
    crud: CRUDBook, db: Session, book: Book, test_book_create: Dict[str, Any]
):
    to_update = crud.get(db, id=99)  # no book with this id

    if to_update is not None:
        pytest.fail("Precondition failed, book with id 99 found")

    with pytest.raises(HTTPException):
        crud.update(db, db_obj=to_update, obj_in=test_book_create)
