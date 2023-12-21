from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base

import pytest
from pydantic import BaseModel


import pytest
from sqlalchemy import Column, Integer, String, create_engine
from typing import Type
from pymongo import MongoClient
from pymongo.collection import Collection
import pymongo
from bson import ObjectId

# Assume the constants like MONGO_URI or MONGO_DB_NAME are defined elsewhere
MONGO_URI = 'your_mongodb_uri'
MONGO_DB_NAME = 'test_db'
FAKE_COLLECTION_NAME = 'fake_collection'


# Simulating the database collection as passed to the function.
# Normally the db_session in the context of pymongo would be a pymongo.collection.Collection instance.
# Note: In a real-world scenario, the db_session parameter would be replaced with the appropriate pymongo collection instance.

def test_create_adds_new_record(db_session: Collection):
    initial_count = db_session.count_documents({})
    new_record = {"created_by": "test_user"}
    result = db_session.insert_one(new_record)
    assert result.inserted_id is not None
    assert db_session.count_documents({}) == initial_count + 1

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703158870842"


# Assuming you have these functions and classes in the actual test scope
# from app.crud.base import CRUDBase
# FakeModel = Collection  or some pymongo collection representation
# FakeCreateSchema  = Your Pydantic model or any similar schema validation

def test_create(db_collection: Collection):
    # In pymongo, we typically interact directly with the collection,
    # so instead of a generic CRUDBase, you would have MongoDB specific CRUD operations.
    # For the purpose of the example, we'll keep crud.create signature the same.
    # However, it should be adapted to use pymongo's collection methods like insert_one

    # To represent the input schema, we transform it to dict as pymongo doesn't use pydantic models
    document_data = {"created_by": "test_user"}
    
    # Insert the document into the collection
    insert_result = db_collection.insert_one(document_data)
    
    # We can check if a new document was added by checking insert_result.inserted_id
    assert insert_result.inserted_id is not None
    
    # Fetch the inserted object to make sure it exists in the collection
    db_obj = db_collection.find_one({"_id": insert_result.inserted_id})
    
    # Verify that the object fetched is indeed the one we inserted
    assert db_obj is not None
    assert db_obj["created_by"] == "test_user"

Base = declarative_base()

# Assuming the db_collection is provided by some fixture or setup in tests
@pytest.fixture
def db_collection(mongo_client):
    db = mongo_client['test_database']  
    collection = db['test_collection']   
    yield collection  
    # Teardown code to clear the collection after tests
    db.drop_collection('test_collection')


class FakeModel(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    created_by = Column(String)


class FakeCreateSchema(BaseModel):
    created_by: str


@pytest.fixture(scope="module")
def db_session() -> Collection:
    # Setup MongoDB client and database. Assuming pymongo has been installed.
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    
    # Create a collection for testing.
    collection = db[FAKE_COLLECTION_NAME]
    
    # Yield the collection to the test functions.
    yield collection
    
    # Dropping the collection after tests are done.
    db.drop_collection(FAKE_COLLECTION_NAME)
    client.close()
