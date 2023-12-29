#
#import pytest
#
#from app.crud.crud_author_plain import *
#
#
#from datetime import date
#
#from app.models.author import Author
#from unittest.mock import MagicMock
#
## It's understood that other necessary imports are already in the file as the class CRUDAuthor and
## its method get_by_author_id are directly accessible.
#
#
## Fixture to mock the database session
#@pytest.fixture
#def mock_db_session():
#    session = MagicMock()
#    return session
#
#
#class TestCRUDAuthor:
#    def test_get_by_author_id_no_errors(self, mock_db_session):
#        # Given
#        crud_author = CRUDAuthor()
#        author_id = 1
#
#        # When
#        result = crud_author.get_by_author_id(mock_db_session, author_id)
#
#        # Then
#        mock_db_session.query.assert_called_with(Author)
#        mock_db_session.query.return_value.filter.assert_called()
#        mock_db_session.query.return_value.filter.return_value.first.assert_called()
#
#    def test_get_by_author_id_with_existing_author(self, mock_db_session):
#        # Given
#        crud_author = CRUDAuthor()
#        author_id = 1
#        test_author = Author(id=author_id, name="Test Author", joined_date=date.today())
#        mock_db_session.query.return_value.filter.return_value.first.return_value = (
#            test_author
#        )
#
#        # When
#        author = crud_author.get_by_author_id(mock_db_session, author_id)
#
#        # Then
#        assert (
#            author == test_author
#        ), "The function should return the correct author object."
#
#    def test_get_by_author_id_with_non_existing_author(self, mock_db_session):
#        # Given
#        crud_author = CRUDAuthor()
#        author_id = 99
#        mock_db_session.query.return_value.filter.return_value.first.return_value = None
#
#        # When
#        author = crud_author.get_by_author_id(mock_db_session, author_id)
#
#        # Then
#        assert (
#            author is None
#        ), "The function should return None for a non-existing author."
#