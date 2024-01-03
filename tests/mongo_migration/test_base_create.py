from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy import Column, Integer, String, create_engine
import pytest
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel as PydanticBaseModel


import pytest
from pymongo.collection import Collection
from app.crud.base import DummyCreateSchema, CRUDBase
import pymongo

# Use the mongo_collection fixture in the test
test_create_with_none_created_by = pytest.mark.usefixtures("mongo_collection")(test_create_with_none_created_by)

Base = declarative_base()



class DummyCreateSchema(PydanticBaseModel):
    data: str
    created_by: Optional[str] = None


def test_create_with_none_created_by(mongo_collection: Collection):
    # Assuming 'DummyCreateSchema' is a Pydantic model that can also be converted to a dictionary for MongoDB insertion
    obj_in_data = DummyCreateSchema(data="some_data").dict(by_alias=True)
    # MongoDB automatically creates an '_id' field, but 'created_by' should be absent, so don't include it in the document.
    insert_result = mongo_collection.insert_one(obj_in_data)
    # Fetch the newly created document using the insert_result.inserted_id
    db_obj = mongo_collection.find_one({"_id": insert_result.inserted_id})
    # Assert that 'created_by' field is None or not present in the document
    assert 'created_by' not in db_obj or db_obj['created_by'] is None, "created_by should be None when not provided."


@pytest.fixture(scope="module")
def db_session():
    # MongoDB connection details
    MONGODB_URI = "mongodb://username:password@localhost:27017/test_db"
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
     
    # This example assumes the presence of a 'dummy_collection' for our DummyModel
    # Normally, you should have a collection for each of your models/entities
    yield db.dummy_collection
    
    # Cleanup: Drop the collection or the entire database as needed after tests
    client.drop_database("test_db")
    # You could also drop only the specific collection used by the tests
    # db.drop_collection('dummy_collection')


class DummyModel(Base):
    __tablename__ = "dummy_model"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    created_by = Column(String, nullable=True)



def test_create_without_errors(db_collection: Collection):
    obj_in = DummyCreateSchema(data="some_data", created_by="user1")  # Assuming this still applies
    db_obj_id = CRUDBase(DummyModel).create(db_collection, obj_in=obj_in)  # DummyModel should have relevant MongoDB schema representation
    
    # Assume CRUDBase.create() returns the inserted_id of the new document
    assert db_obj_id is not None, "The create method should return an object ID."

    # Retrieve the actual document from the database to make sure the insert was successful
    inserted_obj = db_collection.find_one({"_id": db_obj_id})
    assert inserted_obj is not None, "The object should be found in the database after creation."
    assert inserted_obj["data"] == "some_data", "The object data should match the input."
    assert inserted_obj["created_by"] == "user1", "The created_by field should match the input."

# Assuming we have a fixture that provides a pymongo collection (similar to db_session for SQLAlchemy)
@pytest.fixture
def mongo_collection():
    db = client['test_database']  # Replace 'test_database' with actual database name
    collection = db['test_collection']  # Replace 'test_collection' with actual collection name
    yield collection
    # Teardown (e.g., drop the collection)
    db.drop_collection('test_collection')
