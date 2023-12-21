from unittest.mock import MagicMock
from app.models.author import Author

from app.crud.crud_author_plain import CRUDAuthor

import pytest
from app.crud.crud_author_plain import CRUDAuthor
from unittest.mock import MagicMock

from app.crud.crud_author_plain import *
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
from pymongo.collection import Collection


@pytest.fixture
def db_session_mock():
    """Fixture for creating a mock database session."""
    session = MagicMock(spec=Session)
    session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        []
    )
    return session


# Fixtures for PyMongo should not require a 'spec' as in SQLAlchemy's MagicMock
@pytest.fixture
def authors_data():
    """Fixture for mocked authors data."""
    return [{"_id": ObjectId(), "name": f"Author{_}", "email": f"author{_}@example.com"} for _ in range(10)]


@pytest.fixture
def crud_author():
    """Fixture for CRUDAuthor class instance."""
    return CRUDAuthor()


def test_get_no_exceptions(crud_author, db_session_mock):
    """Test CRUDAuthor.get does not raise exceptions and returns a list."""
    result = None
    try:
        result = crud_author.get(db=db_session_mock)
    except Exception as e:
        pytest.fail(f"An error has occurred: {e}")
    assert result is not None


def test_get_return_value(crud_author, db_session_mock, authors_data):
    """Test CRUDAuthor.get returns a list of authors."""
    # Assuming that db_session_mock is a MagicMock instance for MongoDB Collection
    db_session_mock.find.return_value.skip.return_value.limit.return_value.to_list.return_value = authors_data
    authors = crud_author.get(db_session_mock)
    assert isinstance(authors, list)


def test_get_with_skip_limit(crud_author, db_session_mock, authors_data):
    """Test CRUDAuthor.get with custom skip and limit."""
    db_session_mock.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        authors_data
    )
    skip = 5
    limit = 5
    authors = crud_author.get(db=db_session_mock, skip=skip, limit=limit)
    db_session_mock.query.assert_called_once()
    db_session_mock.query.return_value.offset.assert_called_with(skip)
    db_session_mock.query.return_value.offset.return_value.limit.assert_called_with(
        limit
    )
    assert len(authors) == len(authors_data)
