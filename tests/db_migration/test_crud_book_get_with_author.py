#
#from app.crud.crud_book import *
#from sqlalchemy.orm import Session
#
#import pytest
#
#
#from datetime import date
#from app.models.author import Author
#from app.models.book import Book
#from unittest.mock import MagicMock
#
#
## Define a pytest fixture for the database session
#@pytest.fixture(scope="module")
#def mocked_db_session():
#    # Return a mock object of the SQLAlchemy Session
#    session = MagicMock(spec=Session)
#    return session
#
#
## First test to ensure calling the function doesn't produce errors
#def test_get_with_author_no_errors(mocked_db_session):
#    crud_book = CRUDBook()
#    # Mock the database session with chained methods used in the function
#    mocked_db_session.query().join().all.return_value = []
#    response = crud_book.get_with_author(mocked_db_session)
#    # Check that the function returns a value, which is not None
#    assert response is not None
#
#
## Test to check if a call to the function returns a list of Book tuples as expected
#def test_get_with_author_return_values(mocked_db_session):
#    expected_books = [(1, "Book Title", 100, date(2021, 1, 1), 1, "Author Name")]
#    crud_book = CRUDBook()
#    mocked_db_session.query().join().all.return_value = expected_books
#    books = crud_book.get_with_author(mocked_db_session)
#
#    # Check if the returned value is a list
#    assert isinstance(books, list)
#    # Check if all elements in the list are tuples and match the structure of the query return
#    for book in books:
#        assert isinstance(book, tuple)
#        assert len(book) == 6
#        assert isinstance(book[0], int)  # id
#        assert isinstance(book[1], str)  # title
#        assert isinstance(book[2], int)  # pages
#        assert isinstance(book[3], date)  # created_at
#        assert isinstance(book[4], int)  # author_id
#        assert isinstance(book[5], str)  # author_name
#