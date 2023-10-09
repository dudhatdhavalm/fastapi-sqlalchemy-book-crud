from app.crud.book import CRUDBook
from typing import Dict

import pytest
from app.schemas.book import BookCreate
from sqlalchemy.orm import Session
from app.crud.crud_book_plain import *
from app.models.book import Book
from pymongo import MongoClient
from pymongo.database import Database
from bson.objectid import ObjectId
from pymongo.collection import Collection

from app.crud.crud_book_mongo import *


@pytest.fixture()
def db_session() -> Database:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database
    yield db
    client.close()


@pytest.fixture
def crud_book() -> CRUDBook:
    client = MongoClient('localhost', 27017)
    db = client['test_database']
    return CRUDBook(db['test_collection'])


def test_create(db: MongoClient, test_book_data: Dict, crud_book: CRUDBook):
    book_create = BookCreate(**test_book_data)
    
    book_collection: Collection = db["test_db"]["book"]
    inserted_id = crud_book.create(book_collection, obj_in=book_create)
    new_book = book_collection.find_one({"_id": inserted_id})

    assert new_book["title"] == test_book_data["title"]
    assert new_book["pages"] == test_book_data["pages"]
    assert new_book["author_id"] == test_book_data["author_id"]
    assert isinstance(new_book["created_at"], date)


@pytest.fixture
def test_book_data() -> Dict:
    return {"title": "Test book title", "pages": 300, "author_id": 1}
