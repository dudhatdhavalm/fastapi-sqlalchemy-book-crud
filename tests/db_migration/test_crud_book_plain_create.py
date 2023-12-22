

from datetime import date
from app.db.base_class import Base
from app.models.book import Book

from app.crud.crud_book_plain import *
from sqlalchemy import create_engine

import pytest
from sqlalchemy.orm import sessionmaker
from app.schemas.book import BookCreate

from app.crud.crud_book_plain import CRUDBook
from datetime import date
from app.crud.crud_book_plain import CRUDBook

# Connect to the test database
ENGINE_URL = (
    "sqlite:///:memory:"  # For testing purposes, using an in-memory SQLite database
)
engine = create_engine(ENGINE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    # Create a new database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def book_data():
    return BookCreate(title="Test Book", pages=123, author_id=1)


@pytest.fixture(scope="function")
def crud_book():
    return CRUDBook()


def test_create_no_errors(crud_book, db_session, book_data):
    assert crud_book.create(db_session, obj_in=book_data) is not None


def test_create_book_correct_title(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.title == "Test Book"


def test_create_book_correct_pages(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.pages == 123


def test_create_book_correct_author_id(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.author_id == 1


def test_create_book_correct_created_at(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.created_at == date.today()
