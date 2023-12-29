#from unittest.mock import Mock
#from sqlalchemy.orm import Session
#from app.schemas.author import AuthorCreate
#
#import pytest
#
#from app.crud.crud_author import CRUDAuthor
#
#from app.crud.crud_author import *
#from app.models.author import Author
#
#
#from unittest.mock import Mock, patch
#
#
#@pytest.fixture()
#def author_create_data():
#    return {"name": "Test Author", "bio": "Test Bio"}
#
#
#@pytest.fixture()
#def author_create_schema(author_create_data):
#    return AuthorCreate(**author_create_data)
#
#
#@pytest.fixture()
#def db_session():
#    session = Mock(spec=Session)
#    return session
#
#
#@pytest.fixture()
#def mock_author_model():
#    mock_model = Mock(spec=Author)
#    mock_model.id = 1
#    return mock_model
#
#
#@pytest.mark.parametrize(
#    "input_data",
#    [
#        {"name": "Test Author", "bio": "Test Bio"},
#        {},  # Let's test how it behaves with an empty dict
#    ],
#)
#def test_create_author(db_session, input_data, mock_author_model):
#    # Mocking `AuthorCreate` schema since we have a sample data.
#    # We are not testing the schema itself since it should be done in another test.
#    with patch("app.models.author.Author", return_value=mock_author_model):
#        author_create_schema = AuthorCreate(**input_data)
#        crud_author = CRUDAuthor()
#        # since the method `create` relies on `AuthorCreate` schema and the `Session` object,
#        # that's all we need to supply together with the patch for the `Author` model.
#
#        # The test will pass as long as no exceptions are thrown and `result` is not None.
#        result = crud_author.create(db=db_session, obj_in=author_create_schema)
#        assert result is not None
#
#        # Additional validations to ensure the mock objects are utilised correctly.
#        assert db_session.add.called
#        assert db_session.commit.called
#        assert db_session.refresh.called
#