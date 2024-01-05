import pytest
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.crud.base import CRUDBase

from app.crud.base import *

from app.crud.base import CRUDBase
from sqlalchemy import Column, Integer


import pytest
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from pymongo.collection import Collection

# Import fixture(s) and class(es) you may need from the original code context

# Define this constant with the MongoDB connection string
MONGO_DATABASE_URI = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'



class FakeModel(BaseModel):
    name: str


FakeBase = declarative_base()


class FakeORMModel(FakeBase):
    __tablename__ = "fake_table"  # Fake table name for ORM model
    id = Column(
        Integer, primary_key=True
    )  # At least one primary key column is required


@pytest.fixture
def fake_orm_model():
    return FakeORMModel


@pytest.fixture
def fake_db_session():
    client = MongoClient(MONGO_DATABASE_URI)
    db = client.get_database('code_robotics_1704487699809')  # Assuming the database name from the URI
    yield db
    # Cleanup actions if needed, like dropping test collections
    client.close()


def test_crud_base_init(fake_orm_model, fake_db_session):
    """
    Test CRUDBase __init__ method to check if it doesn't raise errors when initialized.
    """
    try:
        crud_base_instance = CRUDBase(model=fake_orm_model)
    except Exception as e:
        pytest.fail(f"CRUDBase __init__ raised an exception: {e}")
    assert crud_base_instance is not None, "CRUDBase instance should not be None."
