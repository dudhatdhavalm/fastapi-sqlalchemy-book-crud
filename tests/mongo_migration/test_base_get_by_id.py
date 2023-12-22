from app.crud.base import *
from app.db.base_class import Base
from sqlalchemy import Column, Integer
from app.crud.base import CRUDBase

from app.crud.base import CRUDBase

import pytest


from unittest.mock import create_autospec
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
import pymongo
from bson.objectid import ObjectId
from unittest.mock import MagicMock
from bson import ObjectId


class ExampleModel(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)


@pytest.fixture
def db_session():
    return create_autospec(Session, instance=True)


@pytest.fixture
def crud_base_instance():
    return CRUDBase(ExampleModel)


def test_get_by_id_no_error(db_session, crud_base_instance):
    db_session.query.return_value.filter.return_value.first.return_value = (
        ExampleModel()
    )
    result = crud_base_instance.get_by_id(db_session, 1)
    assert result is not None


# Assuming ExampleModel has a corresponding MongoDB collection named 'example_model'
# The crud_base_instance would be an instance of a class similar to CRUDBase
# but designed to work with pymongo rather than SQLAlchemy.

def test_get_by_id_correct_item(mongo_collection, crud_base_instance):
    # Create an example document with a mock ObjectId
    example_instance = {'_id': ObjectId(), 'name': 'test_name', 'value': 'test_value'}
    # Let's assume we have a function that adds the document to the MongoDB collection
    inserted_id = mongo_collection.insert_one(example_instance).inserted_id
    
    # Mock the pymongo collection object within the crud_base_instance
    crud_base_instance.collection = mongo_collection
    
    # Now we can perform the actual test where we find the document by its ID
    result = crud_base_instance.get_by_id(inserted_id)
    # The result should be a dictionary, just as it is retrieved from MongoDB
    assert result == example_instance


def test_get_by_id_session_called(db_session, crud_base_instance):
    db_session.query.return_value.filter.return_value.first.return_value = (
        ExampleModel()
    )
    crud_base_instance.get_by_id(db_session, 1)
    db_session.query.assert_called_with(ExampleModel)
    db_session.query(ExampleModel).filter.assert_called()


# Assume ExampleModel is a collection in the MongoDB database.

def test_get_by_id_item_not_found(db_session, crud_base_instance):
    # Set up the MongoDB mock to return None for any ID search.
    db_session.find_one.return_value = None

    # Use an arbitrary number as ID which should not be found in the collection.
    result = crud_base_instance.get_by_id(db_session, 999)
    assert result is None
