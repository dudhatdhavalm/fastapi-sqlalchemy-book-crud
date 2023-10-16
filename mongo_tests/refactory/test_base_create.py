from sqlalchemy import create_engine
from app.db.base_class import Base
from app.crud.base import *
from sqlalchemy.orm import sessionmaker


from pydantic import BaseModel
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId


# Initialize MongoDB client
client = MongoClient('localhost', 27017)

# Get database instance
db = client['test_db']


# Create a fixture for the database session
@pytest.fixture(scope="module")
def dbsession():
    """ Provides a MongoDB Connection

    Returns:
    client – MongoClient for the default host and port.
    """
    client = MongoClient("mongodb://localhost:27017/")
    return client['BooksDB']



# Create a fixture for a sample object to insert
@pytest.fixture(scope='module')
def sample_object() -> Dict[str, Union[int, str]]:
    return {
        'name': 'Test Object',
        'description': 'This is a test object',
        'created_by': 'pytest'
    }


# Define the test case
def test_create(db, sample_object):
    crudbase_obj = SampleCRUDBase()
    result = crudbase_obj.create(
        db, obj_in=sample_object, created_by=sample_object["created_by"]
    )
    assert result is not None
    assert result.name == sample_object["name"]
    assert result.description == sample_object["description"]
    assert result.created_by == sample_object["created_by"]


# Sample CRUDBase class for test
class SampleCRUDBaseModel(BaseModel):
    name: str
    description: str


class SampleCRUDBase(CRUDBase):
    def __init__(self):
        super().__init__(SampleCRUDBaseModel)
