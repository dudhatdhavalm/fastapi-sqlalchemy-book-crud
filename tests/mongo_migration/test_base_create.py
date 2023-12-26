from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import pytest


from typing import Optional

import pytest

from app.crud.base import *
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
import mongomock
from pymongo import MongoClient
from pymongo.collection import Collection
import pymongo
from bson.objectid import ObjectId

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703603283683"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="module")
def db_session() -> MongoClient:
    """Fixture to create a session with the test MongoDB."""
    client = mongomock.MongoClient()
    db = client['test_db']
    try:
        yield db
    finally:
        client.close()


@pytest.fixture(scope="module")
def crud_base() -> CRUDBase:
    class ModelTest(Base):
        __tablename__ = "model_test"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
        description = Column(String, index=True)
        created_by = Column(String, index=True)

    ModelTest.metadata.create_all(bind=engine)

    return CRUDBase(model=ModelTest)


class CreateSchemaType(BaseModel):
    name: str
    description: Optional[str] = None


@pytest.fixture(scope="module")
def create_schema() -> CreateSchemaType:
    return CreateSchemaType(name="Test Item", description="A test item description.")


# Assuming the equivalent of CRUDBase, CreateSchemaType, and ModelTest classes
# are already implemented with pymongo compatibility.

def test_create_with_missing_created_by(
    crud_base: CRUDBase, mongo_collection: Collection, create_schema: CreateSchemaType
):
    """Test that the create method behaves correctly when 'created_by' is not provided."""

    # Insert the data without 'created_by' field using pymongo collection
    result = mongo_collection.insert_one(create_schema.dict(exclude={'created_by'}))
    assert result.inserted_id is not None

    # Verify that document is correctly inserted without 'created_by'
    created_obj = mongo_collection.find_one({"_id": result.inserted_id})

    assert created_obj is not None
    assert created_obj['name'] == "Test Item"
    assert created_obj['description'] == "A test item description."
    assert 'created_by' not in created_obj or created_obj['created_by'] is None


def test_create_does_not_raise_error(
    crud_base: CRUDBase, db_session: Session, create_schema: CreateSchemaType
):
    """Test that the create method does not raise an error and returns a non-None object."""
    assert (
        crud_base.create(db_session, obj_in=create_schema, created_by="test_user")
        is not None
    )


def test_create_successful_commit(
    crud_base: CRUDBase, db_session: Session, create_schema: CreateSchemaType
):
    """Test that an object is successfully created and committed to the database."""
    created_obj = crud_base.create(
        db_session, obj_in=create_schema, created_by="test_user"
    )
    assert created_obj is not None
    assert created_obj.name == "Test Item"
    assert created_obj.description == "A test item description."
    assert created_obj.created_by == "test_user"
