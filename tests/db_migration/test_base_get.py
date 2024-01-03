from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.crud.base import *

import pytest

from app.crud.base import CRUDBase
from unittest.mock import MagicMock, create_autospec


from unittest.mock import MagicMock, create_autospec

# In order to write the pytest, we will start by testing if the function `get` does not throw errors when executed
# and if it returns a non-None value.
# We will have to create a mocked `Session` and a mocked `ModelType` as our input since we are not provided with a specific database model.
# We will also need to make sure to create a `CRUDBase` instance with the mocked model.


# Fixture for mocked database session
@pytest.fixture
def db_session():
    return create_autospec(Session, instance=True)


# Fixture for mocked model
@pytest.fixture
def mock_model():
    class MockModel:
        pass

    return MockModel


# Fixture for CRUDBase instance with mocked model
@pytest.fixture
def crud_base_instance(mock_model):
    return CRUDBase(mock_model)


# Unit test to check if `get` method does not throw errors when called with default parameters
def test_get_no_errors_with_default_parameters(crud_base_instance, db_session):
    result = crud_base_instance.get(db_session)
    assert result is not None, "The `get` method should return a non-None result."


# Additional tests for edge cases would include testing with different skip and limit values
# and making sure to handle scenarios where the database might return empty lists or exceptions.


@pytest.mark.parametrize(
    "skip, limit",
    [
        (0, 100),  # The default case
        (
            -1,
            100,
        ),  # Negative skip which should be handled or tested against the actual behavior
        (
            0,
            -1,
        ),  # Negative limit which should also be handled or tested against actual behavior
        (10, 10),  # Non-default, valid skip and limit
        (100, 0),  # Valid skip and a limit of 0
    ],
)
def test_get_with_various_skip_and_limit(crud_base_instance, db_session, skip, limit):
    result = crud_base_instance.get(db_session, skip=skip, limit=limit)
    assert (
        result is not None
    ), f"The `get` method should handle skip={skip} and limit={limit} without throwing errors."


# Test to check if the session's query method is called with the correct model
def test_get_calls_query_with_correct_model(crud_base_instance, db_session, mock_model):
    crud_base_instance.get(db_session)
    db_session.query.assert_called_with(
        mock_model
    ), "The query should be called with the correct model."


# Unit test to check if the offset and limit methods are called with correct parameters on the query object
def test_get_queries_with_correct_parameters(crud_base_instance, db_session):
    skip, limit = 5, 10  # Arbitrary non-default values
    query_mock = db_session.query.return_value
    offset_mock = query_mock.offset.return_value
    limit_mock = offset_mock.limit.return_value
    crud_base_instance.get(db_session, skip=skip, limit=limit)
    query_mock.offset.assert_called_once_with(skip)
    limit_mock.all.assert_called_once(), "The all method should be called after setting offset and limit."
