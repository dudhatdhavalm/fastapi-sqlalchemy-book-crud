from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from app.crud.crud_book_plain import *

import pytest
from app.schemas.book import BookCreate
from app.models.book import Book


@pytest.fixture
def mock_db_session():
    session = create_autospec(Session, instance=True)
    return session


@pytest.fixture
def book_create_data():
    return BookCreate(title="Test Title", pages=123, author_id=1)


@pytest.fixture
def book_instance():
    return Book(title="Test Title", pages=123, author_id=1)


def test_create_does_not_raise_error(mock_db_session, book_create_data):
    """
    Test that the CRUDBook.create method does not raise an error
    when called with valid arguments.
    """
    crud_book = CRUDBook()
    assert crud_book.create(db=mock_db_session, obj_in=book_create_data) is not None


def test_create_book_instance(mock_db_session, book_create_data, book_instance):
    """
    Test that CRUDBook.create method creates a book instance correctly.
    """
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()

    crud_book = CRUDBook()
    book = crud_book.create(db=mock_db_session, obj_in=book_create_data)

    mock_db_session.add.assert_called_once_with(book)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(book)
    assert book.title == book_create_data.title
    assert book.pages == book_create_data.pages
    assert book.author_id == book_create_data.author_id


def test_create_book_date_set(mock_db_session, book_create_data):
    """
    Test that CRUDBook.create method sets the created_at date.
    """
    crud_book = CRUDBook()
    book = crud_book.create(db=mock_db_session, obj_in=book_create_data)

    assert book.created_at is not None


def test_create_with_no_author_id_raises_error(mock_db_session):
    """
    Test that CRUDBook.create method raises validation error when 'author_id' is not provided.
    """
    with pytest.raises(ValueError):
        crud_book = CRUDBook()
        crud_book.create(
            db=mock_db_session, obj_in=BookCreate(title="Test Title", pages=123)
        )


def test_create_with_no_title_raises_error(mock_db_session):
    """
    Test that CRUDBook.create method raises validation error when 'title' is not provided.
    """
    with pytest.raises(ValueError):
        crud_book = CRUDBook()
        crud_book.create(db=mock_db_session, obj_in=BookCreate(pages=123, author_id=1))


# As the tests are defined, any imports required by the test should be included below
from datetime import date
