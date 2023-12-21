#
#
#from datetime import date
#
#from app.crud.crud_book import *
#from app.models.book import Book
#
#import pytest
#from unittest.mock import MagicMock
#from app.schemas.book import BookCreate
#
#from app.schemas.book import BookCreate
#from datetime import date
#from sqlalchemy.orm import Session
#
## content of test_crud_book.py
#
#
## Fixture to create a mock Session object
#@pytest.fixture
#def mock_db_session():
#    mock_session = MagicMock(spec=Session)
#    mock_session.commit = MagicMock()
#    mock_session.add = MagicMock()
#    mock_session.refresh = MagicMock()
#    return mock_session
#
#
## Fixture to create a sample BookCreate object
#@pytest.fixture
#def sample_obj_in():
#    return BookCreate(title="Sample Book", pages=123, author_id=1)
#
#
## Test that the 'create' method on CRUDBook class does not raise any errors.
#def test_create_book_no_errors(mock_db_session, sample_obj_in):
#    crud_book = CRUDBook()
#    result = crud_book.create(db=mock_db_session, obj_in=sample_obj_in)
#    assert result is not None
#
#
## Test that the 'create' method on CRUDBook class calls the Session 'add', 'commit' and 'refresh' methods.
#def test_create_book_session_methods_called(mock_db_session, sample_obj_in):
#    crud_book = CRUDBook()
#    book = crud_book.create(db=mock_db_session, obj_in=sample_obj_in)
#    mock_db_session.add.assert_called_once_with(book)
#    mock_db_session.commit.assert_called_once()
#    mock_db_session.refresh.assert_called_once_with(book)
#
#
## Test that the 'create' method on CRUDBook class returns a Book object with correct attributes.
#def test_create_book_returns_book_object(mock_db_session, sample_obj_in):
#    mock_db_session.refresh.return_value = None
#    crud_book = CRUDBook()
#    book = crud_book.create(db=mock_db_session, obj_in=sample_obj_in)
#    assert isinstance(book, Book)
#    assert book.title == sample_obj_in.title
#    assert book.pages == sample_obj_in.pages
#    assert book.author_id == sample_obj_in.author_id
#
#
## Test that the 'create' method sets the 'created_at' field of the new Book object to today's date.
#def test_create_book_sets_created_at_today(mock_db_session, sample_obj_in):
#    fake_book = Book(
#        title=sample_obj_in.title,
#        pages=sample_obj_in.pages,
#        author_id=sample_obj_in.author_id,
#        created_at=date.today(),
#    )
#    mock_db_session.add.return_value = fake_book
#    mock_db_session.refresh.return_value = None
#    crud_book = CRUDBook()
#    book = crud_book.create(db=mock_db_session, obj_in=sample_obj_in)
#    assert book.created_at == date.today()
#