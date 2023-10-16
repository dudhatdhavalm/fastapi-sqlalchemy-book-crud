from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.book import Book
from typing import Generator
from app.crud.crud_book import *

import pytest
from pymongo import MongoClient
from app.crud.crud_book import CRUDBook
from bson.objectid import ObjectId
from app.mongo_models.book import Book
from app.mongo_crud.crud_book import CRUDBook
import pymongo

client = MongoClient('localhost', 27017)
db = client['test_database']
collection = db['test_collection']


def test_get_multi_skip_and_limit() -> None:
    crud = CRUDBook()
    books = list(collection.find().skip(1).limit(1))
    if collection.count_documents({}) > 1:
        assert len(books) == 1
    else:
        assert len(books) == 0


# Prepare DB session for testing
@pytest.fixture(scope="module")
def db() -> Generator:
    CLIENT = MongoClient("mongodb://localhost:27017/")
    db = CLIENT["BooksDB"]
    yield db
    CLIENT.close()



def test_get_multi_no_error(client: MongoClient) -> None:
    crud = CRUDBook()
    books = crud.get_multi(client)
    assert books is not None



def test_get_multi_skip(db: MongoClient) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, skip=1)
    if db[Book].count_documents({}) > 1:
        assert len(books) == db[Book].count_documents({}) - 1
    else:
        assert len(books) == 0


def test_get_multi_max_limit(client: MongoClient) -> None:
    crud = CRUDBook()
    books = list(client.db.books.find().limit(100))
    assert len(books) <= 100
