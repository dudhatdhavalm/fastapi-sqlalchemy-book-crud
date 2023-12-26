
from app.crud.crud_book_plain import *

import pytest
from unittest.mock import MagicMock


from unittest.mock import MagicMock
from sqlalchemy.orm import Session

# Since 'get' method belongs to CRUDBook class and uses session object of SQLAlchemy to query, so
# we need to mock the session and Book object which are being used by the 'get' method.


@pytest.fixture
def db_session():
    # Create a MagicMock object to emulate the Session object from SQLAlchemy
    session = MagicMock(spec=Session)

    # Set up the `query` method chain that ends with `all`
    session.query().offset().limit().all.return_value = []

    return session


@pytest.fixture
def crud_book():
    # Instantiate the CRUDBook object
    return CRUDBook()


@pytest.fixture
def skip():
    return 0


@pytest.fixture
def limit():
    return 100


# Test if the function doesn't throw errors when it's executed
def test_get_no_errors(crud_book, db_session, skip, limit):
    result = crud_book.get(db_session, skip=skip, limit=limit)
    assert result is not None, "The 'get' function returned None"


# Test if the function returns a list
def test_get_returns_list(crud_book, db_session, skip, limit):
    result = crud_book.get(db_session, skip=skip, limit=limit)
    assert isinstance(result, list), "The 'get' function should return a list"


# Test with a custom skip and limit values
def test_get_custom_skip_limit(crud_book, db_session):
    custom_skip = 10
    custom_limit = 50
    result = crud_book.get(db_session, skip=custom_skip, limit=custom_limit)
    db_session.query().offset.assert_called_with(custom_skip)
    db_session.query().offset().limit.assert_called_with(custom_limit)
    assert (
        result is not None
    ), "The 'get' function returned None with custom skip and limit"


# Test the 'get' function with default parameters
def test_get_with_default_params(crud_book, db_session):
    result = crud_book.get(db_session)
    db_session.query().offset.assert_called_with(0)
    db_session.query().offset().limit.assert_called_with(100)
    assert (
        result is not None
    ), "The 'get' function returned None with default parameters"


# Test with a negative skip value should not break the function
def test_get_negative_skip(crud_book, db_session):
    negative_skip = -10
    result = crud_book.get(db_session, skip=negative_skip)
    db_session.query().offset.assert_called_with(negative_skip)
    assert (
        result is not None
    ), "The 'get' function returned None with a negative skip value"


# Test with a negative limit value should not break the function
def test_get_negative_limit(crud_book, db_session):
    negative_limit = -10
    result = crud_book.get(db_session, limit=negative_limit)
    db_session.query().offset().limit.assert_called_with(negative_limit)
    assert (
        result is not None
    ), "The 'get' function returned None with a negative limit value"
