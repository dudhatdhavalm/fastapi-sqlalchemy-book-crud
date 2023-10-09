from app.crud.crud_book import *
from datetime import date
from fastapi import HTTPException

import pytest
from sqlalchemy.orm import Session


from typing import Any, Dict
from app.models.book import Book
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from typing import Dict, Any
from contextlib import contextmanager

import pymongo
from pymongo.database import Database
from pymongo.errors import PyMongoError
from pymongo.errors import OperationFailure
from bson import ObjectId


from typing import Any, Dict, Optional



def test_update_book_failure(
    crud: CRUDBook,
    collection_name: str,  # Instead of SQLAlchemy Session
    book: Book,
    test_book_create: Dict[str, Any]
):
    db = MongoClient()["test_db"]
    collection = db[collection_name]

    try:
        to_update = collection.find_one({"_id": ObjectId("some_random_id")})  # no book with this id
    except Exception:
        pytest.fail("Precondition failed, could not fetch book with id some_random_id")

    if to_update is not None:
        pytest.fail("Precondition failed, book with id some_random_id found")

    with pytest.raises(OperationFailure):
        # Assuming the CRUDBook class has been modified to work with pymongo
        crud.update(collection, db_obj=to_update, obj_in=test_book_create)



def test_update_book(crud: CRUDBook, db: MongoClient, book: Dict[str, Any], test_book_create: Dict[str, Any]):
    collection = db["book"]
    to_update = collection.find_one({"_id": book["_id"]})

    if to_update is None:
        pytest.fail("Precondition failed, no book with id 1 found")

    try:
        update_result = collection.update_one({"_id": to_update["_id"]}, {'$set': test_book_create})

        if update_result.modified_count != 1:
            pytest.fail("Update operation failed")
    except PyMongoError as e:
        pytest.fail(f"An error occurred: {str(e)}")

    new_book = collection.find_one({"_id": to_update["_id"]})

    assert new_book["_id"] == to_update["_id"]
    assert new_book["title"] == test_book_create["title"]
    assert new_book["pages"] == test_book_create["pages"]
    assert new_book["description"] == test_book_create["description"]
    assert new_book["author_id"] == test_book_create["author_id"]
    assert new_book["created_at"] == to_update["created_at"]


@pytest.fixture
def db_session() -> Database:
    client = MongoClient('localhost', 27017)
    db = client.test_database
    try:
        yield db
    finally:
        client.close()


@pytest.fixture
def test_book_create() -> Dict[str, Any]:
    return {
        "title": "Test Book",
        "pages": 100,
        "description": "Test Book description",
        "author_id": 1,
    }


@pytest.fixture
def author() -> Dict[str, Any]:
    author = {"_id": 1, "name": "Test Author"}
    client = MongoClient('localhost', 27017)
    db = client['test_database']
    authors_collection = db['authors']
    authors_collection.insert_one(author)
    yield author
    authors_collection.delete_one({"_id": 1})


@pytest.fixture
def book() -> Dict[str, Any]:
    mongo_client = MongoClient(host='localhost', port=27017)
    db = mongo_client['test_database']
    collection = db['books']
    
    new_book = {
        "_id": ObjectId(),
        "title": "Test Book",
        "pages": 100,
        "description": "Test Book description",
        "created_at": datetime.now(),
    }

    collection.insert_one(new_book)

    return new_book
