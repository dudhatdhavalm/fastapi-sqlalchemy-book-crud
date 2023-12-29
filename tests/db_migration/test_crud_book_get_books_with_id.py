#
#from app.crud.crud_book import *
#from sqlalchemy.orm import Session
#
#import pytest
#from datetime import date
#
#
#from datetime import date
#
#from app.models.author import Author
#from app.models.author import Author
#from app.models.book import Book
#from unittest.mock import MagicMock
#
## test_crud_book.py
#
#
#@pytest.fixture(scope="module")
#def test_data():
#    return {
#        "id": 1,
#        "title": "Sample Book",
#        "pages": 123,
#        "created_at": date.today(),
#        "author_id": 1,
#        "author_name": "Sample Author",
#    }
#
#
#@pytest.fixture(scope="module")
#def db_session():
#    # Create a MagicMock with specifications of the Session class
#    session_mock = MagicMock(spec=Session)
#    # Mock the query chain that's used in the get_books_with_id method
#    query_mock = MagicMock()
#    session_mock.query.return_value.join.return_value.filter.return_value.first.return_value = (
#        query_mock
#    )
#    return session_mock
#
#
#@pytest.fixture(scope="module")
#def crud_book():
#    # Use the Book model as a parameter for CRUDBook, following the error hint.
#    return CRUDBook()
#
#
#def test_get_books_with_id_no_error(crud_book, db_session, test_data):
#    """Test if get_books_with_id method executes without error."""
#    db_session.query.return_value.join.return_value.filter.return_value.first.return_value = (
#        test_data
#    )
#    result = crud_book.get_books_with_id(db=db_session, book_id=1)
#    assert result is not None
#
#
#def test_get_books_with_id_invalid_id_type(crud_book, db_session):
#    """Test if get_books_with_id method raises TypeError for invalid book_id type."""
#    with pytest.raises(TypeError):
#        crud_book.get_books_with_id(db=db_session, book_id="not_an_integer")
#
#
#def test_get_books_with_id_not_found(crud_book, db_session):
#    """Test if get_books_with_id method returns None when book is not found."""
#    db_session.query.return_value.join.return_value.filter.return_value.first.return_value = (
#        None
#    )
#    result = crud_book.get_books_with_id(db=db_session, book_id=9999)
#    assert result is None
#