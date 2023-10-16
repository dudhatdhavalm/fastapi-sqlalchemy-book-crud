from app.crud.crud_book_plain import *
import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from app.crud.crud_book import CRUDBook


@pytest.fixture
def db_session() -> Session:
    return Session(
        bind=create_engine("postgresql://postgres:root@localhost:5432/BooksDB")
    )


@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook()


def test_get_books_with_id_no_errors(crud_book: CRUDBook, db_session: Session):
    result = crud_book.get_books_with_id(db_session, 1)
    assert result is not None


def test_get_books_with_id_nonexistent_id(crud_book: CRUDBook, db_session: Session):
    result = crud_book.get_books_with_id(db_session, -1)
    assert result is None


def test_get_books_with_id_invalid_id(crud_book: CRUDBook, db_session: Session):
    with pytest.raises(TypeError):
        crud_book.get_books_with_id(db_session, "abc")
