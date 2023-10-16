from app.crud.crud_book_plain import *
from sqlalchemy import create_engine
from app.models.author import Author
from sqlalchemy.orm import sessionmaker
from app.models.book import Book
from datetime import date

import pytest
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="module")
def db():
    """
    Create a new database session for a test
    """
    engine = create_engine(
        "postgresql://postgres:root@localhost:5432/BooksDB",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()

    yield session

    session.close()


def test_get_with_author(db):
    """
    Test to verify if function 'get_with_author' is compiled
    without raising any exceptions
    """
    CRUD_books = CRUDBook()
    response = CRUD_books.get_with_author(db)
    assert response is not None


def test_get_books_with_author(db):
    """
    Test to verify the functionality of 'get_with_author' with dummy data
    """
    # given
    author = Author(name="Author1")
    db.add(author)
    db.commit()

    book1 = Book(title="Book1", pages=150, created_at=date.today(), author_id=author.id)
    book2 = Book(title="Book2", pages=200, created_at=date.today(), author_id=author.id)
    db.add(book1)
    db.add(book2)
    db.commit()

    # when
    CRUD_books = CRUDBook()
    books = CRUD_books.get_with_author(db)

    # then
    assert len(books) == 2
    assert all([isinstance(book, Book) for book in books])


def test_get_books_with_author_empty(db):
    """
    Test to verify the functionality of 'get_with_author' with no data
    """
    # when
    CRUD_books = CRUDBook()
    books = CRUD_books.get_with_author(db)

    # then
    assert books == []
