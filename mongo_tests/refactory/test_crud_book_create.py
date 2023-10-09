from app.crud.book import CRUDBook
from app.crud.crud_book import *
from typing import Dict

import pytest
from app.schemas.book import BookCreate
from sqlalchemy.orm import Session
from app.models.book import Book
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database


@pytest.fixture(scope="module")
def db_session() -> MongoClient:
    client = MongoClient("mongodb://localhost:27017/")
    yield client
    client.close()


@pytest.fixture
def test_book_data() -> Dict:
    return {"title": "Test book title", "pages": 300, "author_id": 1}


@pytest.fixture
def crud_book() -> CRUDBook:
    client = MongoClient('localhost', 27017)
    db = client.test_database
    return CRUDBook(db)


def test_create(test_book_data: Dict[str, any], crud_book: CRUDBook):
    book_create = BookCreate(**test_book_data)
    collection = db['book']
    new_book_id = collection.insert_one(book_create.dict()).inserted_id
    new_book = collection.find_one({'_id': new_book_id})

    assert new_book['title'] == test_book_data["title"]
    assert new_book['pages'] == test_book_data["pages"]
    assert new_book['author_id'] == test_book_data["author_id"]
    assert isinstance(new_book['created_at'], date)
