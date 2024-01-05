from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Type, Union
from unittest.mock import MagicMock
from pydantic import BaseModel, create_model

from app.crud.base import *

import pytest




from typing import Optional
from pymongo import MongoClient
import pymongo
from pymongo.collection import Collection
from bson import ObjectId
from pydantic import BaseModel

# Define the database connection string provided
MONGO_URI = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'

# Define a MongoDB client according to the provided connection string.
MONGO_DB_URI = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'
client = pymongo.MongoClient(MONGO_DB_URI)
db = client.get_database()  # Get the default database


def test_update_with_no_modifications(crud_base: CRUDBase):
    # Set up the MongoDB client and access the required collection
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    collection = db["your_collection_name"]  # Replace with your actual collection name

    # Create the mock for the CRUDBase with the collection
    crud_base = CRUDBase(collection)
    
    # Create an object to update
    db_obj = {"_id": ObjectId(), "name": "Original Name"}
    collection.insert_one(db_obj)

    # Perform the test
    original_name = db_obj["name"]
    update_data = {"name": original_name}  # No change to name
    updated_obj = crud_base.update(db_obj=db_obj, obj_in=update_data)
    
    assert updated_obj["name"] == original_name  # Name should not change
    
    # Clean up the inserted document
    collection.delete_one({"_id": db_obj["_id"]})
collection_name = 'your_collection'  # The name of the collection to interact with
collection: Collection = db[collection_name]

# MongoDB connection string
MONGO_DB_URI = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'



class ModelType(BaseModel):  # Mocked database model for testing
    id: int
    name: str
    modified_by: Optional[str] = None


UpdateSchemaType = create_model(
    "UpdateSchemaType", name=(str, ...), modified_by=(Optional[str], None)
)


@pytest.fixture()
def db_session() -> MagicMock:
    """Fixture to mock SQLAlchemy Session."""
    return MagicMock(spec=Session)



def test_update_function_execution_without_errors(
    crud_base: CRUDBase, db_obj: ModelType
):
    # Assuming the CRUDBase.update method has been modified to accept PyMongo Collection and ObjectId
    update_data = UpdateSchemaType(name="updated_name", modified_by="updated_user").dict()

    # Let's mock a PyMongo ObjectId for the db_obj
    db_obj_id = ObjectId()

    # Mocking the db_obj to assign it an _id field to simulate a MongoDB document
    db_obj_dict = db_obj.dict()
    db_obj_dict['_id'] = db_obj_id

    # Call the update method, passing in the collection and the mocked ObjectId along with update_data
    updated_obj = crud_base.update(db=collection, db_obj_id=db_obj_id, obj_in=update_data)

    assert updated_obj is not None
    # You can even check if the name and modified_by have been updated
    assert updated_obj['name'] == 'updated_name'
    assert updated_obj['modified_by'] == 'updated_user'


@pytest.fixture()
def crud_base() -> CRUDBase:
    """Fixture to create an instance of CRUDBase with ModelType."""
    client = MongoClient(MONGO_DB_URI)
    db = client.get_default_database()
    collection = db['modeltype']  # Assuming the collection name is 'modeltype'
    return CRUDBase(collection=collection)


@pytest.fixture()
def db_obj() -> ModelType:
    """Fixture to create a fake instance of a SQLAlchemy model."""
    return ModelType(id=1, name="original_name", modified_by="original_user")


def test_update_with_dict_input(
    crud_base: CRUDBase, db_session: MagicMock, db_obj: ModelType
):
    update_data = {"name": "updated_name", "modified_by": "updated_user"}
    updated_obj = crud_base.update(db=db_session, db_obj=db_obj, obj_in=update_data)
    assert updated_obj is not None
