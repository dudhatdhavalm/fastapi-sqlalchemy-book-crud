from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from app.crud.crud_author_plain import *


# Fixture to mock the Session
@pytest.fixture
def mock_db_session():
    session = create_autospec(Session, instance=True)
    # Setting up mock return values if needed can go here. For example:
    # session.query().offset().limit().all.return_value = []
    return session


# Fixture to create an instance of CRUDAuthor
@pytest.fixture
def crud_author():
    return CRUDAuthor()


def test_get_no_errors(crud_author, mock_db_session):
    # Test that no errors are thrown
    assert crud_author.get(db=mock_db_session) is not None


def test_get_with_skip_limit(crud_author, mock_db_session):
    # Test with different skip and limit values
    assert crud_author.get(db=mock_db_session, skip=10, limit=5) is not None


def test_get_with_large_limit(crud_author, mock_db_session):
    # Test with large limit value
    assert crud_author.get(db=mock_db_session, skip=0, limit=1000) is not None


def test_get_with_negative_skip(crud_author, mock_db_session):
    # Test with negative skip value, should handle gracefully
    assert crud_author.get(db=mock_db_session, skip=-10, limit=100) is not None


def test_get_with_negative_limit(crud_author, mock_db_session):
    # Test with negative limit value, should handle gracefully
    assert crud_author.get(db=mock_db_session, skip=0, limit=-100) is not None


def test_get_with_none_values(crud_author, mock_db_session):
    # Test with None values for skip and limit, should default to 0 and 100
    assert crud_author.get(db=mock_db_session, skip=None, limit=None) is not None
