from sqlalchemy import Column, Integer, String, create_engine
import pytest


import pytest
from sqlalchemy.orm import declarative_base, sessionmaker

from app.crud.base import *
from pymongo import MongoClient
from pymongo.collection import Collection
import pymongo

# This would be your MongoDB URI connecting to your database server
# In practice, it might look something like "mongodb://localhost:27017/test_database"
MONGO_URI = "your_mongo_uri"


Base = declarative_base()


class MockModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String)


@pytest.fixture(scope="module")
def testing_engine():
    return create_engine("sqlite:///:memory:")


# The test function is named the same as requested.
def test_CRUDBase_init_without_errors():
    # Assuming a setup for a MongoDB test instance has been done and a test collection acquired.
    # The MongoClient and related setup code would typically come from a fixture or a setup function.
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    test_db = client["test_db"]
    test_collection = test_db["test_collection"]
    
    instance = None

    try:
        instance = CRUDBase(collection=test_collection)
    except Exception as e:
        pytest.fail(f"CRUDBase.__init__ raised an exception with a valid collection: {e}")

    assert (
        instance is not None
    ), "CRUDBase.__init__ should create an instance with a valid collection."


@pytest.fixture(scope="module")
def create_tables(testing_engine):
    Base.metadata.create_all(testing_engine)


@pytest.fixture(scope="function")
def db_session():
    client = MongoClient(MONGO_URI)
    db = client.get_database() # Adjust to get your specific test database
    collection = db.get_collection("test_collection")

    yield collection

    # MongoDB does not have transactions the same way SQL databases do
    # in the traditional sense, so we do not need to handle rollback.
    # For cleanup, drop the collection or database if required.
    db.drop_collection("test_collection")
    client.close()


def test_CRUDBase_init_assigns_model(db_session):
    crud_instance = CRUDBase(model=MockModel)
    assert (
        crud_instance.model == MockModel
    ), "CRUDBase instance should have the model attribute set to MockModel."
