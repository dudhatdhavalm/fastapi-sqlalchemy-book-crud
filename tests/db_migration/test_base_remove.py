#from sqlalchemy.orm import Session
#
#from app.crud.base import *
#
#import pytest
#
#from sqlalchemy import Column, Integer
#
#
#from unittest.mock import MagicMock
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer
#from unittest.mock import MagicMock
#
#from app.crud.base import CRUDBase
#
## Create a base class for declarative class definitions
#Base = declarative_base()
#
#
#@pytest.fixture
#def db_session_mock():
#    session = MagicMock(spec=Session)
#    session.query.return_value.get.return_value = MagicMock()
#    return session
#
#
#@pytest.fixture
#def test_model():
#    # A dummy subclass of Base with a primary key column to simulate a SQLAlchemy model
#    class TestModel(Base):
#        __tablename__ = "test_model"
#        id = Column(Integer, primary_key=True)  # Simulate a primary key column
#
#    return TestModel
#
#
#@pytest.fixture
#def crud_base_instance(test_model):
#    return CRUDBase(model=test_model)
#
#
#def test_remove_no_errors(crud_base_instance, db_session_mock):
#    """
#    Test that the remove function executes without errors.
#    """
#    # Simulate behavior when an object with ID exists
#    db_session_mock.query.return_value.get.return_value = Base()
#    assert crud_base_instance.remove(db=db_session_mock, id=1) is not None
#
#
#def test_remove_nonexistent_id(crud_base_instance, db_session_mock):
#    """
#    Test that remove function behaves correctly when a nonexistent ID is used.
#    """
#    db_session_mock.query.return_value.get.return_value = None
#    assert crud_base_instance.remove(db=db_session_mock, id=999) is None
#
#
#def test_remove_object(crud_base_instance, db_session_mock):
#    """
#    Test that remove function calls delete and commit on the session.
#    """
#    test_entity = Base()
#    db_session_mock.query.return_value.get.return_value = test_entity
#
#    removed_entity = crud_base_instance.remove(db=db_session_mock, id=1)
#
#    # Assertions to ensure the correct calls were made on the DB session
#    db_session_mock.delete.assert_called_once_with(test_entity)
#    db_session_mock.commit.assert_called_once()
#    assert (
#        removed_entity is test_entity
#    ), "The returned object should be the test entity"
#