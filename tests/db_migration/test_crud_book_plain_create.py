# Assuming the database models emulate SQLAlchemy's declarative base
# begin imports
from datetime import date
from app.schemas.book import BookCreate

from app.crud.crud_book_plain import *
from app.crud.crud_book_plain import CRUDBook
from unittest.mock import MagicMock
from app.models.book import Book

# Import necessary libraries and modules for pytest tests
import pytest

# end imports


# Create a fixture to mock the database session
@pytest.fixture
def mock_db_session():
    class MockSession:
        def add(self, obj):
            pass

        def commit(self):
            pass

        def refresh(self, obj):
            obj.id = 1  # Simulate the object being refreshed from the database

    return MockSession()


# Create a fixture for the book data
@pytest.fixture
def book_data():
    return BookCreate(title="Sample Book", pages=123, author_id=1)


# Test if CRUDBook.create can run without errors
def test_create_runs_without_errors(mock_db_session, book_data):
    crud_book = CRUDBook()
    # Use a mock object here to prevent actual database interaction
    book = crud_book.create(db=mock_db_session, obj_in=book_data)
    assert book is not None


# Test if CRUDBook.create sets created_at date
def test_create_sets_created_at(mock_db_session, book_data):
    crud_book = CRUDBook()
    book = crud_book.create(db=mock_db_session, obj_in=book_data)
    assert book.created_at == date.today()


# Test if CRUDBook.create adds a new book to the session
def test_create_adds_book_to_session(mock_db_session, book_data):
    mock_db_session.add = MagicMock()
    crud_book = CRUDBook()
    crud_book.create(db=mock_db_session, obj_in=book_data)
    # Check if the session's add method was called once
    mock_db_session.add.assert_called_once()


# Test if CRUDBook.create commits the session
def test_create_commits_session(mock_db_session, book_data):
    mock_db_session.commit = MagicMock()
    crud_book = CRUDBook()
    crud_book.create(db=mock_db_session, obj_in=book_data)
    # Check if the session's commit method was called
    mock_db_session.commit.assert_called_once()


# Test if CRUDBook.create refreshes the new book object
def test_create_refreshes_book_object(mock_db_session, book_data):
    mock_db_session.refresh = MagicMock()
    crud_book = CRUDBook()
    crud_book.create(db=mock_db_session, obj_in=book_data)
    # Check if the session's refresh method was called once with the book object
    mock_db_session.refresh.assert_called_once()
