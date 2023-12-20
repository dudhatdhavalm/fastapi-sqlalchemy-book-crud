#
#import pytest
#from app.crud.crud_book_plain import CRUDBook
#from app.crud.crud_book_plain import *
#from app.models.book import Book
#from app.models.author import Author
#from sqlalchemy.exc import OperationalError
#from sqlalchemy.orm import Session, sessionmaker
#from unittest.mock import MagicMock
#
#
#@pytest.fixture
#def mock_db_session():
#    db = MagicMock(spec=Session)
#    yield db
#
#
#@pytest.fixture
#def crud_book():
#    return CRUDBook()
#
#
## Test the function not throwing error in normal execution
#def test_get_books_with_id_no_errors(mock_db_session, crud_book):
#    book_id = 1
#    result = crud_book.get_books_with_id(mock_db_session, book_id)
#    assert result is not None
#
#
## Test when there's no book with the provided id
#def test_get_books_with_id_book_id_not_exists(mock_db_session, crud_book):
#    book_id = -1
#    result = crud_book.get_books_with_id(mock_db_session, book_id)
#    assert result is None
#
#
## Test with proper data and expects to get the correct output
#def test_get_books_with_id_correct_output(mock_db_session, crud_book: CRUDBook):
#    # Setup
#    author = Author(id=1, name="Author 1")
#    book = Book(id=1, title="Book 1", pages=100, created_at=date.today(), author_id=1)
#
#    mock_db_session.query().join().filter().first().return_value = {
#        "id": 1,
#        "title": "Book 1",
#        "pages": 100,
#        "created_at": date.today(),
#        "author_id": 1,
#        "author_name": "Author 1",
#    }
#
#    # Get book with id
#    result = crud_book.get_books_with_id(mock_db_session, 1)
#    result = dict(result)
#
#    assert result["id"] == 1
#    assert result["title"] == "Book 1"
#    assert result["pages"] == 100
#    assert result["created_at"] == date.today()
#    assert result["author_id"] == 1
#    assert result["author_name"] == "Author 1"
#