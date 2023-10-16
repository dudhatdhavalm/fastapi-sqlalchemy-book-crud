import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from app.crud.base import *


from typing import Generator
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from pymongo.errors import InvalidId



def test_remove_with_non_integer_id(db: MongoClient) -> None:
    crud_base = CRUDBase(db)
    try:
        crud_base.remove(id="non integer id")
    except Exception as e:
        assert isinstance(e, InvalidId)


def test_remove_with_invalid_id(db: Session) -> None:
    crud_base = MongoClient().test_database.crud_base
    try:
        crud_base.delete_one({"id": 999999})
    except PyMongoError as e:
        assert isinstance(e, PyMongoError)



def test_remove(db) -> None:
    collection = db['test_collection']
    obj_id = ObjectId()
    obj = collection.insert_one({'_id': obj_id})
    result = db.test_collection.delete_one({'_id': obj.inserted_id})
    assert result.deleted_count == 1


@pytest.fixture(scope="module")
def db() -> Generator:
    host = os.getenv("MONGO_HOST", "localhost")
    port = os.getenv("MONGO_PORT", 27017)
    client = MongoClient(host, port)
    db_ = client.get_database("BooksDB")
    yield db_
    client.close()
