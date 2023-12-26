from sqlalchemy.ext.declarative import declarative_base

from app.crud.base import CRUDBase

import pytest
from unittest.mock import Mock, create_autospec
from unittest.mock import create_autospec

from app.crud.base import *
from typing import Any, Type, TypeVar
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session




from typing import Type, TypeVar
from pymongo import MongoClient
from pymongo.collection import Collection
import mongomock


Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


@pytest.fixture
def mock_db_session() -> Session:
    """
    Fixture for creating a mock database session.
    """
    return create_autospec(Session, instance=True)


# Defining the fixture to make use of mongomock for MongoDB
@pytest.fixture
def crud_base_instance() -> CRUDBaseMongo:
    """
    Fixture for creating a CRUDBaseMongo instance with DummyModel collection.
    """
    client = mongomock.MongoClient()
    db = client['mydb']
    collection = db['dummymodel']
    return CRUDBaseMongo(collection=collection)


def test_get_by_id_does_not_raise_error(
    crud_base_instance: CRUDBase, mock_db_session: Session
):
    """
    Test if calling get_by_id does not raise any exceptions and it doesn't return None when it shouldn't.
    """
    mock_db_session.query.return_value.filter.return_value.first.return_value = (
        DummyModel()
    )
    try:
        result = crud_base_instance.get_by_id(mock_db_session, 1)
        assert result is not None
    except Exception as ex:
        pytest.fail(f"get_by_id raised an exception: {ex}")
