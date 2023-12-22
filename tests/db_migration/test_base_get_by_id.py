
from app.crud.base import *
from app.db.base_class import Base
from sqlalchemy import Column, Integer
from app.crud.base import CRUDBase

from app.crud.base import CRUDBase

import pytest


from unittest.mock import create_autospec
from unittest.mock import create_autospec
from sqlalchemy.orm import Session


# Sample SQLAlchemy model class for testing
class ExampleModel(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)


# Create fixture for database session
@pytest.fixture
def db_session():
    return create_autospec(Session, instance=True)


# Fixture for the CRUDBase instance with ExampleModel
@pytest.fixture
def crud_base_instance():
    return CRUDBase(ExampleModel)


# Test to check whether `get_by_id` does not throw errors and returns a non-None value
def test_get_by_id_no_error(db_session, crud_base_instance):
    db_session.query.return_value.filter.return_value.first.return_value = (
        ExampleModel()
    )
    result = crud_base_instance.get_by_id(db_session, 1)
    assert result is not None


# Test to check if `get_by_id` correctly uses the session to query the model
def test_get_by_id_session_called(db_session, crud_base_instance):
    db_session.query.return_value.filter.return_value.first.return_value = (
        ExampleModel()
    )
    crud_base_instance.get_by_id(db_session, 1)
    db_session.query.assert_called_with(ExampleModel)
    db_session.query(ExampleModel).filter.assert_called()


# Test to handle cases where the item is not found
def test_get_by_id_item_not_found(db_session, crud_base_instance):
    db_session.query.return_value.filter.return_value.first.return_value = None
    result = crud_base_instance.get_by_id(db_session, 999)
    assert result is None


# Test to ensure that the correct item is returned
def test_get_by_id_correct_item(db_session, crud_base_instance):
    example_instance = ExampleModel()
    db_session.query.return_value.filter.return_value.first.return_value = (
        example_instance
    )
    result = crud_base_instance.get_by_id(db_session, example_instance.id)
    assert result == example_instance
