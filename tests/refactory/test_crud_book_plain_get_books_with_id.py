from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import Session, sessionmaker
from app.models.author import Author


from datetime import date

import pytest
from app.crud.crud_book_plain import *
from app.models.book import Book


# Create a database connection and session for the tests
@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("postgresql://localhost/BooksDB")
    connection = engine.connect()
    connection.execute(
        """CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                            title VARCHAR(100),
                            pages INTEGER,
                            created_at DATE,
                            author_id INTEGER
                        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS authors (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR(100)
                        )"""
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal


# Create a test object of CRUDBook
@pytest.fixture(scope="module")
def test_crud_book():
    return CRUDBook()


# Test case for existing book id
def test_get_books_with_id_existing(test_db: Session, test_crud_book: CRUDBook):
    # Given
    book1 = Book(
        id=1, title="Book1", pages=100, created_at=date(2020, 5, 17), author_id=1
    )
    author1 = Author(id=1, name="Author1")
    test_db.add_all([author1, book1])
    test_db.commit()

    # When
    result = test_crud_book.get_books_with_id(test_db, 1)

    # Then
    assert result.id == 1
    assert result.title == "Book1"


# Test case for non-existing book id
def test_get_books_with_id_non_existing(test_db: Session, test_crud_book: CRUDBook):
    # Given - No data in db

    # When
    result = test_crud_book.get_books_with_id(test_db, 99)

    # Then
    assert result is None
