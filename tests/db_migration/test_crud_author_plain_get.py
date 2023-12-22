

from unittest.mock import MagicMock
from app.models.author import Author

import pytest
from unittest.mock import MagicMock

from app.crud.crud_author_plain import *
from sqlalchemy.orm import Session


# Fixture for creating a mock database session
@pytest.fixture(scope="function")
def mock_db_session():
    session = MagicMock(spec=Session)
    session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        Author(),
        Author(),
    ]
    return session


# Test to check if the function doesn't throw errors when it's executed
def test_get_without_errors(mock_db_session):
    crud_author = CRUDAuthor()
    assert crud_author.get(mock_db_session) is not None


# Test with different skip and limit parameters
def test_get_with_different_parameters(mock_db_session):
    crud_author = CRUDAuthor()
    skip = 10
    limit = 5
    result = crud_author.get(mock_db_session, skip=skip, limit=limit)
    assert mock_db_session.query.called
    query = mock_db_session.query.return_value
    assert query.offset.called_with(skip)
    assert query.limit.called_with(limit)
    assert result is not None


# Test for no authors case
def test_get_no_authors(mock_db_session):
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        []
    )
    crud_author = CRUDAuthor()
    result = crud_author.get(mock_db_session)
    assert result == []


# Test to check if an incorrect parameter raises a TypeError
def test_get_incorrect_parameters(mock_db_session):
    crud_author = CRUDAuthor()
    with pytest.raises(TypeError):
        # Here we intentionally pass a string instead of an integer to trigger a TypeError
        crud_author.get(mock_db_session, skip="invalid", limit="invalid")


# Edge case: very high skip value
def test_get_with_high_skip(mock_db_session):
    crud_author = CRUDAuthor()
    result = crud_author.get(mock_db_session, skip=10**6, limit=20)
    # The list returned might be empty in case of a high skip, but should not throw an error
    assert result is not None
