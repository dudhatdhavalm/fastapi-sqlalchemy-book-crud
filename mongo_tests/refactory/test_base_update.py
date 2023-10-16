from sqlalchemy import create_engine
from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from pydantic import BaseModel
from app.crud.base import *


from typing import Generic, Type, TypeVar

import pytest
from pymongo import MongoClient
from bson import ObjectId
from typing import Any, Dict

# Prepare required imports for the test
ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)








class TestCRUDBase:
    @pytest.fixture
    def db(self):
        DB_URL = "postgresql://postgres:root@localhost:5432/BooksDB"
        engine = create_engine(DB_URL)
        session = sessionmaker(bind=engine)()
        yield session
        session.close()


    def test_update_no_errors(self):
        mongo_client = MongoClient('mongodb://localhost:27017/')
        db = mongo_client['mydatabase']
        collection = db['mycollection']

        class SampleModel:
            def __init__(self, id: Any, name: str):
                self.id = id
                self.name = name

        class SampleSchema:
            def __init__(self, name: str):
                self.name = name

        sample_instance = SampleModel(ObjectId(), "Initial")
        updated_sample_schema = SampleSchema(name="Updated")

        collection.insert_one(sample_instance.__dict__)
        
        result = collection.update_one(
            { "_id": sample_instance.id },
            { "$set": updated_sample_schema.__dict__ }
        )

        assert result.matched_count > 0


    def test_update_obj_in_dict(self):
        class SampleModel:
            id: int
            name: str

        # Create a MongoDB client, change the << MONGODB URL >> with your MongoDB Atlas url or localhost url 
        client = MongoClient("<< MONGODB URL >>")

        # Create a database and collection to perform operations
        database = client['myDatabase']
        SampleModel_collection = database['sample_model']

        # Create an instance of the SampleModel
        sample_instance = SampleModel()
        sample_instance.id = str(ObjectId())
        sample_instance.name = "Initial"

        # Insert the instance into the MongoDB collection
        SampleModel_collection.insert_one(sample_instance.__dict__)

        # Update instance
        updated_sample_dict = {"name": "Updated"}

        result = SampleModel_collection.find_one_and_update(
            {"_id": sample_instance.id},
            {"$set": updated_sample_dict},
            return_document=True)

        assert result is not None

        # Clean up by deleting the data
        SampleModel_collection.delete_one({"_id": sample_instance._id})

        # Close the connection
        client.close()
