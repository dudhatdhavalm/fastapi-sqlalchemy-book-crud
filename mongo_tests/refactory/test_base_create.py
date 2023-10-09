from app.db.base_class import Base
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, sessionmaker
from app.crud.base import *
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union


import pytest

import pytest
from sqlalchemy.orm import Session


from typing import Any, Dict, Generator, Generic, List, Optional, Type, TypeVar, Union
from app.crud.base import CRUDBase

from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from contextlib import contextmanager
from bson import ObjectId
from typing import Dict
from pymongo.database import Database

ModelType = TypeVar("ModelType")

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")








class CRUDBase(Generic[ModelType, CreateSchemaType]):

    @staticmethod
    def create(
        collection, *, obj_in : Dict, created_by: Optional[str] = None
    ) -> Dict:
        """
        Insert a new document into a MongoDB collection.
        Returns the new document.

        Args:
            collection: The MongoDB collection.
            obj_in : Document to be inserted.
            created_by (Optional[str], optional): The creator of the document. Defaults to None.
            
        Returns:
            Dict: Returns the created document.
        """
        obj_in["created_by"] = created_by
        return collection.insert_one(obj_in).inserted_id


    def __init__(self, collection_name: str) -> None:
        pymongo_client = MongoClient('mongodb://localhost:27017/')
        db = pymongo_client["your_database_name"]  # Replace with your actual DB name
        self.collection = db[collection_name]
      
    def get(self, id: Any) -> Optional[ModelType]:
        return self.collection.find_one({"_id": id})

    def get_multi(self, *, skip=0, limit=100) -> List[ModelType]:
        return list(self.collection.find().skip(skip).limit(limit))
      
    def update(self, *, id: Any, obj_in: Dict) -> ModelType:
        self.collection.update_one({"_id": id}, {"$set": obj_in})
        return self.collection.find_one({"_id": id})

    def remove(self, id: Any) -> ModelType:
        return self.collection.delete_one({"_id": id})

# Initialize test data
test_data = {"field1": "value1", "field2": "value2"}


def test_create(client: MongoClient):
    # Create an object of class CRUDBase
    test_crud = CRUDBase('test_base_collection')

    # Create a new data row using the 'create' method
    new_base = test_crud.create(client=client, obj_in=test_data, created_by="test_user")

    assert isinstance(new_base, Dict)
    assert new_base['_id'] is not None  # In pymongo, the '_id' field is created automatically
    assert new_base['field1'] == test_data["field1"]
    assert new_base['field2'] == test_data["field2"]
    assert new_base['created_by'] == "test_user"


@pytest.fixture(scope="module")
def test_db() -> Generator:
    # Set up a new database for testing
    client = MongoClient("mongodb://localhost:27017/")
    db = client["BooksDB"]

    yield db  # this is where the testing happens

    # Clean-up code (delete all documents and close connection)
    client.drop_database('BooksDB')
    client.close()
