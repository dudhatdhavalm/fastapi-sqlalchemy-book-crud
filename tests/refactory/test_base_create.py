from sqlalchemy import create_engine
from app.db.base_class import Base
from app.crud.base import *
from sqlalchemy.orm import sessionmaker


from pydantic import BaseModel
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

import pytest


# Create a fixture for the database session
@pytest.fixture(scope="module")
def dbsession():
    engine = create_engine("postgresql://postgres:root@localhost:5432/BooksDB")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


# Create a fixture for a sample object to insert
@pytest.fixture(scope="module")
def sample_object() -> Dict[str, Union[int, str]]:
    return {
        "name": "Test Object",
        "description": "This is a test object",
        "created_by": "pytest",
    }


# Sample CRUDBase class for test
class SampleCRUDBaseModel(BaseModel):
    name: str
    description: str


class SampleCRUDBase(CRUDBase):
    def __init__(self):
        super().__init__(SampleCRUDBaseModel)


# Define the test case
def test_create(dbsession, sample_object):
    crudbase_obj = SampleCRUDBase()
    result = crudbase_obj.create(
        dbsession, obj_in=sample_object, created_by=sample_object["created_by"]
    )
    assert result is not None
    assert result.name == sample_object["name"]
    assert result.description == sample_object["description"]
    assert result.created_by == sample_object["created_by"]
