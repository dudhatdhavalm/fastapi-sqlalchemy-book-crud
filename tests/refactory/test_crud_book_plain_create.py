from app.schemas.book import BookCreate
from app.models.book import Book
from sqlalchemy.orm import Session, sessionmaker
from datetime import date
from sqlalchemy import create_engine

import pytest
from app.models.author import Author
from app.crud.crud_book_plain import *

engine = create_engine("postgresql://localhost/BooksDB")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture to provide SQLAlchemy session
@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fixture to provide CRUDBook instance
@pytest.fixture(scope="function")
def crud_book():
    from app.crud.crud_book_plain import CRUDBook

    return CRUDBook()


# test case to verify create function
def test_create_book(crud_book, db_session):
    author = Author(name="Test Author")

    db_session.add(author)
    db_session.commit()

    book_create = BookCreate(title="Sanity Test", pages=150, author_id=author.id)
    result = crud_book.create(db_session, obj_in=book_create)

    assert result is not None, "Expected book, received None"
    assert isinstance(
        result, Book
    ), "Expected instance of Book, received different object"
    assert result.title == "Sanity Test", "Book title does not match"
    assert result.pages == 150, "Book pages does not match"
    assert result.author_id == author.id, "Book's author id does not match"


# test case to verify exception in case of missing title in create function
def test_create_with_missing_title(crud_book, db_session):
    author = Author(name="Test Author")

    db_session.add(author)
    db_session.commit()

    book_create = BookCreate(title=None, pages=150, author_id=author.id)
    with pytest.raises(Exception):
        crud_book.create(db_session, obj_in=book_create)


# test case to verify exception in case of missing pages in create function
def test_create_with_missing_pages(crud_book, db_session):
    author = Author(name="Test Author")

    db_session.add(author)
    db_session.commit()

    book_create = BookCreate(title="Sanity Test", pages=None, author_id=author.id)
    with pytest.raises(Exception):
        crud_book.create(db_session, obj_in=book_create)


# test case to verify exception in case of missing author_id in create function
def test_create_with_missing_author_id(crud_book, db_session):
    book_create = BookCreate(title="Sanity Test", pages=150, author_id=None)
    with pytest.raises(Exception):
        crud_book.create(db_session, obj_in=book_create)
