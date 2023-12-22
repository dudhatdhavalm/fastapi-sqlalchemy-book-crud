from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, MetaData, String, create_engine


import pytest
import pytest

from sqlalchemy import Column, Integer, MetaData, create_engine
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson.objectid import ObjectId

# Assuming Mongo URI and options would be defined here or imported from a config
MONGO_URI = 'mongodb://localhost:27017'
DATABASE_NAME = 'test_database'
COLLECTION_NAME = 'test_collection'

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
engine = create_engine(DATABASE_URL)


def test_remove_no_errors(mongodb_db: Database, collection_name: str):
    collection: Collection = mongodb_db[collection_name]

    # Insert a new object/document into the collection
    insert_result = collection.insert_one({})
    inserted_id = insert_result.inserted_id

    # Verify the object is indeed present in the collection
    obj = collection.find_one({'_id': inserted_id})
    assert obj is not None, "Object should be present in the collection"

    # Use the delete method to remove the object from the collection
    delete_result = collection.delete_one({'_id': inserted_id})
    
    # Check that the delete operation was acknowledged and one document was deleted
    assert delete_result.acknowledged, "Remove operation should be acknowledged"
    assert delete_result.deleted_count == 1, "One document should be deleted"
    
    # Verify the object is no longer present in the collection
    assert collection.find_one({'_id': inserted_id}) is None, "Object should be deleted from the collection"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


@pytest.fixture(scope='module')
def db_session():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Setup code here, like creating indexes if necessary
    # ...

    try:
        yield collection
    finally:
        # Tear down code; drop the test collection or database
        db.drop_collection(COLLECTION_NAME)
        client.close()


@pytest.fixture(scope="module")
def crud_base_instance(db_session):
    instance = CRUDBase(DummyModel)
    yield instance
