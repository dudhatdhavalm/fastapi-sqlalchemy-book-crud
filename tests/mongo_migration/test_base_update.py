from sqlalchemy.orm import sessionmaker

from app.crud.base import *

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, String, create_engine


from typing import Optional
from pydantic import BaseModel
from typing import Any, Dict, Type, Union
from sqlalchemy.ext.declarative import declarative_base
import pymongo
from pymongo.collection import Collection
from pymongo import MongoClient
from pymongo.collection import ReturnDocument
from app.crud.base import crud_base
from app.models.dummy_model import DummyModel, UpdateSchema

# Setup pymongo database connection (you might need to adjust connection details)
client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']  # test_database is an example database name

# Define the collection where the DummyModel documents will be stored
dummy_collection = db['dummy_collection']  # dummy_collection is an example collection name

# Assuming that the Mongo client, db name, and collection name are predefined.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
TEST_DB_NAME = 'test_db'


# The db_session should now be a MongoDB database session/collection
@pytest.mark.parametrize(
    "update_data",
    [
        ({"name": "Test1", "modified_by": "User1"}),
        ({"name": "Test2"}),
        (UpdateSchema(name="Test3").dict()),
        (UpdateSchema(name="Test4", modified_by="User4").dict()),
    ],
)
def test_update_various_inputs(db_session: Collection, update_data):
    # Create a dummy document in the collection
    dummy_db_obj = {"name": "Old Name"}
    result = db_session.insert_one(dummy_db_obj)
    dummy_db_obj_id = result.inserted_id

    # The 'crud_base' needs to be adapted for PyMongo usage
    updated_obj = crud_base.update(
        collection=db_session, obj_id=dummy_db_obj_id, obj_in=update_data
    )

    # Fetch the updated document from the collection
    updated_document = db_session.find_one({"_id": dummy_db_obj_id})

    assert updated_document is not None, "The document should have been updated."
    assert updated_document.get("name") == update_data.get("name"), "The 'name' field should have been updated."

    # Ensure that 'modified_by' is updated if provided in update_data, otherwise it shouldn't exist in document
    if "modified_by" in update_data:
        assert updated_document.get("modified_by") == update_data.get("modified_by"), "The 'modified_by' field should have been updated."
    else:
        assert "modified_by" not in updated_document, "The 'modified_by' field should not exist in the document."
TEST_COLLECTION_NAME = 'test_collection'

client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)

Base = declarative_base()


def test_update_no_errors():
    # Insert a dummy object into the database
    dummy_db_obj = {"name": "Old Name"}
    insert_result = dummy_collection.insert_one(dummy_db_obj)
    assert insert_result.inserted_id is not None  # Make sure the insert succeeded

    # Prepare the update object
    dummy_update_obj = {"$set": {"name": "New Name", "modified_by": "Updater"}}
    
    # Update the object in the database
    updated_obj = dummy_collection.find_one_and_update(
        {"_id": insert_result.inserted_id},  # Filter to identify the document to update
        dummy_update_obj,
        return_document=ReturnDocument.AFTER  # Return the modified document
    )

    # Check that the update was applied
    assert updated_obj is not None
    assert updated_obj.get('name') == 'New Name'
    assert updated_obj.get('modified_by') == 'Updater'


class DummyModel(Base):
    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    modified_by = Column(String)


class UpdateSchema(BaseModel):
    name: str
    modified_by: Optional[str] = None


DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    db = client[TEST_DB_NAME]
    collection = db[TEST_COLLECTION_NAME]
    collection.drop()  # Make sure we start with a clean state
    try:
        yield collection
    finally:
        collection.drop()  # Clean up after testing


crud_base = CRUDBase(model=DummyModel)
