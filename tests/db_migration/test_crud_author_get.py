#
#import pytest
#from unittest.mock import MagicMock, create_autospec
#from app.crud.crud_author import CRUDAuthor
#
#from app.crud.crud_author import *
#
#
#from unittest.mock import MagicMock, create_autospec
#from sqlalchemy.orm import Session
#
#
## Assuming that CRUDAuthor takes a model as a constructor argument
#@pytest.fixture(scope="module")
#def crud_author(db_model):
#    return CRUDAuthor(model=db_model)
#
#
#@pytest.fixture(scope="module")
#def db_model():
#    from app.models.author import Author
#
#    return Author
#
#
#@pytest.fixture(scope="module")
#def mock_db_session():
#    db_session = create_autospec(Session)
#    query_mock = db_session.query.return_value
#    offset_mock = query_mock.offset.return_value
#    limit_mock = offset_mock.limit.return_value
#    limit_mock.all.return_value = []
#    return db_session
#
#
#def test_get_no_errors(crud_author, mock_db_session):
#    result = crud_author.get(db=mock_db_session, skip=0, limit=100)
#    assert result is not None
#
#
#def test_get_query_calls(mock_db_session, crud_author, db_model):
#    # We will use the `configure_mock` method to setup our mock to account for chaining
#    db_session_query = mock_db_session.query
#    db_session_query.configure_mock(
#        **{"return_value.offset.return_value.limit.return_value.all.return_value": []}
#    )
#
#    result = crud_author.get(db=mock_db_session, skip=10, limit=10)
#
#    # Check that the right sequence of method calls was made
#    db_session_query.assert_called_once_with(db_model)
#    db_session_query.return_value.offset.assert_called_once_with(10)
#    db_session_query.return_value.offset.return_value.limit.assert_called_once_with(10)
#
#    # Check that the final method in the chain, 'all', was called to fetch the results
#    db_session_query.return_value.offset.return_value.limit.return_value.all.assert_called_once()
#
#    # The result variable is currently not being used after assignment.
#    # We can assert that it was returned properly as an empty list,
#    # as it was set up in the `mock_db_session` fixture.
#    assert (
#        result
#        == db_session_query.return_value.offset.return_value.limit.return_value.all.return_value
#    )
#