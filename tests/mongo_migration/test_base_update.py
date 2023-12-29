from typing import Type

import pytest
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from pydantic import BaseModel, create_model
from sqlalchemy import Column, Integer, String, create_engine

from app.crud.base import *


from typing import Type
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.crud.base import CRUDBase # Assuming this is updated to use PyMongo

Base = declarative_base()


class ExampleModel(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    modified_by = Column(Integer)


ExampleSchema = create_model("ExampleSchema", name=(str, ...), modified_by=(int, ...))


DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="function")
def example_model(db: Collection) -> dict:
    example_obj = {"name": "Old Name", "modified_by": 1}
    result = db.insert_one(example_obj)
    example_obj['_id'] = result.inserted_id
    return example_obj
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope="function")
def db() -> Database:
    # Using a mock client for demonstration, which simulates a MongoDB instance in memory.
    # Replace 'MockMongoClient()' with 'MongoClient()' to use a real MongoDB instance.
    client = MockMongoClient()

    # Here 'test_database' is the name of your test database, change it accordingly.
    db = client.test_database

    # Perform any setup tasks, if required, e.g., creating collections or indices
    # ExampleModel would be a collection in the MongoDB test_database 
    db.ExampleModel.create_index("some_field_name")

    # Yield the database object to the test case.
    yield db

    # Cleanup tasks, drop the test database after tests run.
    client.drop_database('test_database')
    client.close()


@pytest.fixture(scope="function")
def crud_base() -> CRUDBase:
    return CRUDBase(model=ExampleModel)




class TestCRUDBase:

    def test_update_no_errors(
        self, db: Database, collection_name: str, example_document, crud_base: CRUDBase
    ):
        """
        Test if CRUDBase.update method executes without raising any errors
        with valid arguments in a PyMongo context.
        """
        example_collection: Collection = db[collection_name]
        update_obj = {"name": "New Name", "modified_by": 2}

        # Assuming CRUDBase has been adapted for pymongo, and update now works with pymongo collections
        try:
            result = crud_base.update(
                collection=example_collection,
                filter_dict={'_id': example_document['_id']},
                update_dict={'$set': update_obj},
                modified_by=2
            )
            assert result is not None
        except Exception as e:
            pytest.fail(f"Update method raised an exception: {e}")
