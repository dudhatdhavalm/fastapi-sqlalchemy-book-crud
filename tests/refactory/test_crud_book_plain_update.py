from app.crud.crud_book_plain import *
import pytest
from sqlalchemy.orm import Session
from app.models.author import Author
from app.models.book import Book


@pytest.fixture(scope="function")
def db():
    db = Session()
    yield db
    db.close()


@pytest.fixture
def db_book():
    book = Book(title="Test Book", year="2020", author_id=1, created_at=date.today())
    yield book


@pytest.fixture
def update_book():
    return {"title": "Updated Test Book", "year": "2021", "author_id": 1}


def test_update(db, db_book, update_book):
    crud_book = CRUDBook()
    updated_book = crud_book.update(db, db_obj=db_book, obj_in=update_book)
    assert updated_book is not None
    assert updated_book.title == "Updated Test Book"
    assert updated_book.year == "2021"
    assert updated_book.author_id == 1
    assert isinstance(updated_book.created_at, date)
    assert updated_book.created_at == date.today()


def test_update_with_no_valid_db_obj(db, update_book):
    crud_book = CRUDBook()
    try:
        crud_book.update(db, db_obj=None, obj_in=update_book)
    except Exception as e:
        assert isinstance(e, TypeError)


def test_update_with_no_valid_obj_in(db, db_book):
    crud_book = CRUDBook()
    try:
        crud_book.update(db, db_obj=db_book, obj_in=None)
    except Exception as e:
        assert isinstance(e, TypeError)
