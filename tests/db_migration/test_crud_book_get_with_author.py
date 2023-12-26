#from app.models.book import Book
#
#import pytest
#from unittest.mock import MagicMock, patch
#from app.crud.crud_book import CRUDBook
#
#from app.crud.crud_book import *
#
#
#from datetime import date
#from app.models.author import Author
#from sqlalchemy.orm import Session
#
#
#@pytest.fixture
#def mocked_db_session():
#    db_session = MagicMock(spec=Session)
#    query_mock = db_session.query.return_value
#
#    # Mock join to return the query itself as chain methods don't cause attribute error
#    query_mock.join.return_value = query_mock
#    # Mock all to return a list of Book objects
#    query_mock.all.return_value = [
#        (1, "Title 1", 123, date(2020, 1, 1), 1, "Author Name 1"),
#        (2, "Title 2", 456, date(2021, 2, 2), 2, "Author Name 2"),
#    ]
#
#    return db_session
#
#
#def test_get_with_author_no_error(mocked_db_session):
#    with patch("app.crud.crud_book.CRUDBase") as MockedCRUDBase:
#        MockedCRUDBase.return_value = MagicMock()
#        crud_book = CRUDBook()
#        result = crud_book.get_with_author(mocked_db_session)
#        assert result is not None
#        # Additional assertions can be made about the type and contents of the result
#        assert isinstance(result, list), "Result should be a list"
#        for item in result:
#            assert isinstance(item, tuple), "Each item in the result should be a tuple"
#