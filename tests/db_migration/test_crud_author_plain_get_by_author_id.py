#from sqlalchemy.orm import Session, scoped_session, sessionmaker
#from app.crud.crud_author_plain import *
#
#from app.crud.crud_author import CRUDAuthor
#from unittest.mock import MagicMock
#
#import pytest
#
#
#class FakeAuthor:
#    def __init__(self, id=None, name=None, book=None, birthdate=None):
#        self.id = id
#        self.name = name
#        self.book = book
#        self.birthdate = birthdate
#
#
#@pytest.fixture(scope="function")
#def mock_db_session():
#    return MagicMock(spec=Session)
#
#
#@pytest.fixture(scope="function")
#def mock_author():
#    return FakeAuthor(1, "John Doe", "book_1", "1990-1-1")
#
#
#def test_get_by_author_id(mock_db_session, mock_author):
#    # Arrange
#    mock_db_session.query().filter().first.return_value = mock_author
#    crud_author = CRUDAuthor()
#
#    # Act
#    result = crud_author.get_by_author_id(db=mock_db_session, id=1)
#
#    # Assert
#    assert result is not None
#    mock_db_session.query.assert_called_once_with(CRUDAuthor.get_by_author_id.model)
#    mock_db_session.query().filter.assert_called_once_with(mock_author.id == 1)
#    mock_db_session.query().filter().first.assert_called_once()
#
#
#def test_get_by_author_id_nonexistent(mock_db_session):
#    # Arrange
#    mock_db_session.query().filter().first.return_value = None
#    crud_author = CRUDAuthor()
#
#    # Act
#    result = crud_author.get_by_author_id(db=mock_db_session, id=1)
#
#    # Assert
#    assert result is None
#    mock_db_session.query.assert_called_once_with(CRUDAuthor.get_by_author_id.model)
#    mock_db_session.query().filter.assert_called_once_with(mock_author.id == 1)
#    mock_db_session.query().filter().first.assert_called_once()
#