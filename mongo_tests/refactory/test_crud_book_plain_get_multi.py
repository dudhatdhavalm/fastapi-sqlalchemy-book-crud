from app.crud.crud_book_plain import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.book import Book
from typing import Generator

import pytest
from pymongo import MongoClient
from app.crud.crud_book import CRUDBook
from typing import Dict, List
from bson.objectid import ObjectId


# Prepare DB session for testing
@pytest.fixture(scope="module")
def db() -> Generator:
    MONGO_DB_URL = "mongodb://localhost:27017/BooksDB"
    client = MongoClient(MONGO_DB_URL)
 
    db = client.test
    yield db
    db.client.close()



def test_get_multi_max_limit(db: MongoClient) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, limit=100)
    assert books.count_documents({}) <= 100


def test_get_multi_skip_and_limit(db: MongoClient) -> None:
    crud = CRUDBook()
    books = list(db.books.find().skip(1).limit(1))
    if db.books.count_documents({}) > 1:
        assert len(books) == 1
    else:
        assert len(books) == 0


def test_get_multi_skip(db: MongoClient, book_collection: str) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, skip=1, book_collection=book_collection)
    if db[book_collection].count_documents({}) > 1:
        assert len(books) == db[book_collection].count_documents({}) - 1
    else:
        assert len(books) == 0


def test_get_multi_no_error() -> None:
    client = MongoClient()  # you might need to provide host and port here
    db = client.test_database  # replace with your database name
    crud = CRUDBook()
    books = crud.get_multi(db.books)  # replace 'books' with your collection name
    assert books is not None
