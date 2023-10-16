from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base


import pytest
from app.crud.base import *
from typing import Any

import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.database import Database
from app.crud.base import CRUDBase

# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient(port=27017)
db = client.test

# Setup the test database
DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_get_invalid_id_type(test_db: MongoClient, crud_base_class: CRUDBasePymongo):
    with pytest.raises(Exception):
        crud_base_class.get(test_db, "invalid_id")


def test_get_nonexistent_id(test_db: Database , crud_base_class):
    result = crud_base_class.get(test_db, 1000000)
    assert result is None


def test_get_negative_id(test_db: MongoClient, generic_collection: str):
    with pytest.raises(Exception):
        test_db[generic_collection].find_one({"_id": ObjectId(-1)})


def test_get_failure(test_db: MongoClient, crud_base_class: CRUDBase):
    result = crud_base_class.get(test_db, 0)
    assert result is None




def test_get_success(test_db: Database, crud_base_class: MongoCRUDBase):
    result = crud_base_class.get(test_db, {"_id": 1})
    assert result is not None

Base.metadata.create_all(bind=engine)



# Fixture for the database session
@pytest.fixture(scope="module")
def test_db():
    db = MongoClient("mongodb://localhost:27017/")["test_database"]
    try:
        yield db
    finally:
        db.client.close()


@pytest.fixture(scope="module")
def crud_base_class():
    return CRUDBase(db)
