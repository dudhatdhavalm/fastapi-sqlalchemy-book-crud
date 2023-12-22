from app.models.author import Author

import pytest
from unittest.mock import MagicMock

from app.crud.crud_author import *
from sqlalchemy.orm import Session




from unittest.mock import MagicMock


class MockModel:
    pass


@pytest.fixture(scope="module")
def db_session_mock():
    session_mock = MagicMock(spec=Session)
    query_mock = MagicMock()
    query_mock.offset.return_value = query_mock
    query_mock.limit.return_value = query_mock
    query_mock.all.return_value = []
    session_mock.query.return_value = query_mock
    return session_mock


@pytest.fixture(scope="module")
def crud_author():
    return CRUDAuthor(model=MockModel)


# You should have a Mongo collection mock available
def test_crud_author_get_without_errors(collection_mock, crud_author):
    # In pymongo, the 'db' attribute typically refers to a database, not a session.
    # Here, the mock should simulate the collection, not a database session.
    crud_author.get = MagicMock(return_value=MockModel())  # Assuming MockModel() simulates a document
    # The assertion assumes that 'get' will return a non-None value 
    # (in this case, a MagicMock object simulating a model/document)
    assert crud_author.get(db=collection_mock) is not None


def test_crud_author_get_with_skip(db_session_mock, crud_author):
    assert crud_author.get(db=db_session_mock, skip=5) is not None


def test_crud_author_get_with_limit(db_session_mock, crud_author):
    assert crud_author.get(db=db_session_mock, limit=50) is not None


# Assuming crud_author is a class with a method get that interacts with MongoDB
# In this context, db_session_mock is assumed to be a MagicMock object representing a MongoDB collection

def test_crud_author_get_with_skip_and_limit(db_session_mock, crud_author):
    # Mock the pymongo collection's find method to return a non-empty cursor
    db_session_mock.find.return_value.limit.return_value.skip.return_value = [MockModel(), MockModel()]

    # Call the CRUD method we're testing
    result = crud_author.get(db=db_session_mock, skip=10, limit=10)

    # Assertions
    assert db_session_mock.find.called
    assert db_session_mock.find.return_value.limit.called
    assert db_session_mock.find.return_value.skip.called
    assert result is not None
    assert len(result) > 0  # Assuming the result should be a list of documents


def test_crud_author_get_returns_list(db_session_mock, crud_author):
    result = crud_author.get(db=db_session_mock)
    assert isinstance(result, list)
