import pytest
from app.crud.base import CRUDBase

from app.crud.base import *

from app.crud.base import CRUDBase
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, sessionmaker


import pytest
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import ObjectId
import pymongo

# Suppose the collection name in MongoDB is 'dummy_collection'
collection_name = 'dummy_collection'

# PyMongo Client Setup
client = pymongo.MongoClient('mongodb://root:example@localhost:27017/')
db = client.code_robotics_1704487699809
dummy_collection = db.dummy_collection  # Assuming 'dummy_collection' represents DummyModel documents

Base = declarative_base()


# Making the assumption that a fixture setup for database session/connection, 'db_session'
# would return a PyMongo database connection, and 'crud_base_instance' would handle MongoDB operations
# with an equivalent MongoClient setup.


@pytest.mark.parametrize("test_id", [2, "not-an-id", None])
def test_get_by_id_invalid_id(crud_base_instance, db_session, test_id):
    # Convert ID to a string that should be compatible with MongoDB ObjectId
    # In real cases, you would handle the conversion or checks differently depending on your application logic
    try:
        mongo_test_id = ObjectId(str(test_id))
    except Exception:  # If ObjectId creation fails, we assume 'test_id' is invalid for MongoDB
        mongo_test_id = test_id

    # Assuming 'get_by_id' in 'crud_base_instance' has been adjusted to work with PyMongo
    result = crud_base_instance.get_by_id(db_session[collection_name], mongo_test_id)
    assert (
        result is None
    ), f"get_by_id should return None for non-existent or invalid ID: {test_id}"


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def crud_base_instance():
    # We provide the MongoDB collection instead of a SQLAlchemy model
    return MongoCRUDBase(dummy_collection)


# Use a context manager to handle the MongoDB connection setup and teardown
@pytest.fixture(scope="function")
def db_session():
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    db = client['code_robotics_1704487699809']
    
    # You can choose to clear the collection or database before running each test
    # Example: db.drop_collection('DummyModel')
    # Or perform any setup tasks if required

    yield db

    # Perform any teardown tasks if required
    # Example: db.drop_collection('DummyModel')
    client.close()


def test_get_by_id_no_errors(crud_base_instance, db_session):
    dummy_object = DummyModel(id=1)
    db_session.add(dummy_object)
    db_session.commit()

    result = crud_base_instance.get_by_id(db_session, 1)
    assert (
        result is not None
    ), "get_by_id should return a non-None result when a matching ID is found."
