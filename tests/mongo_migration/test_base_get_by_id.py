# Import statements for dependencies
from unittest.mock import create_autospec

from app.crud.base import *

import pytest


from unittest.mock import create_autospec
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer

# Define a base class using the SQLAlchemy declarative system
Base = declarative_base()


# Dummy SQLAlchemy model to be used with CRUDBase
class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


# Define a fixture for the database session
@pytest.fixture
def fake_db_session():
    """Provide a fake database session for testing purposes."""
    return create_autospec(Session)


# Define a fixture for the CRUD base instance
@pytest.fixture
def crud_base_instance():
    """Provide a CRUD base instance with a dummy model."""
    return CRUDBase(model=DummyModel)


def test_get_by_id_no_errors(crud_base_instance, fake_db_session):
    """Test if get_by_id executes without errors."""
    mocked_query = fake_db_session.query.return_value
    mocked_query.filter.return_value.first.return_value = DummyModel()
    result = crud_base_instance.get_by_id(fake_db_session, 1)
    assert (
        result is not None
    ), "get_by_id should return a result or None, but should not raise an error"
