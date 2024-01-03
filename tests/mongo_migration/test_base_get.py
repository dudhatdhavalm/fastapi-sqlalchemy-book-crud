from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.crud.base import *

import pytest

from app.crud.base import CRUDBase
from unittest.mock import MagicMock, create_autospec


from unittest.mock import MagicMock, create_autospec
from unittest.mock import MagicMock



@pytest.fixture
def db_session():
    return create_autospec(Session, instance=True)


@pytest.fixture
def mock_model():
    class MockModel:
        pass

    return MockModel


@pytest.fixture
def crud_base_instance(mock_model):
    return CRUDBase(mock_model)


def test_get_no_errors_with_default_parameters(crud_base_instance, db_session):
    result = crud_base_instance.get(db_session)
    assert result is not None, "The `get` method should return a non-None result."




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


def test_get_calls_query_with_correct_model(crud_base_instance, db_session, mock_model):
    crud_base_instance.get(db_session)
    db_session.query.assert_called_with(
        mock_model
    ), "The query should be called with the correct model."


# Assuming the imports below are provided as the test function is part of a larger test suite with access to these fixtures
# from tests.conftest import crud_base_instance, db_session

def test_get_queries_with_correct_parameters(crud_base_instance, db_session):
    skip, limit = 5, 10  # Arbitrary non-default values
    collection_mock = MagicMock()
    db_session.return_value = collection_mock
    find_mock = collection_mock.find.return_value
    skip_mock = find_mock.skip.return_value
    limit_mock = skip_mock.limit.return_value
    crud_base_instance.get(db_session, skip=skip, limit=limit)
    collection_mock.find.assert_called_once()
    find_mock.skip.assert_called_once_with(skip)
    limit_mock.to_list.assert_called_once_with(None), "The to_list method should be called after setting skip and limit."
