import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.crud.crud_author import *
from app.models.author import Author


import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId


@pytest.fixture(scope="module")
def db_session():
    DATABASE_URL = "mongodb://localhost:27017"
    client = MongoClient(DATABASE_URL)
    database = client["BooksDB"]
    try:
        yield database
    finally:
        client.close()



@pytest.fixture(scope="module")
def new_author(db_session: MongoClient):
    author = Author(id=1, name="John Doe", book="Test Book")
    db_session.authors.insert_one(author.__dict__)
    return author




def test_get_not_exists(db_session: Session):
    crud_author = CRUDAuthor()
    author = crud_author.get(db_session, 9999)
    assert author is None


def test_get_exists(client: MongoClient, new_author: dict):
    crud_author = client['database']['author']
    author = crud_author.find_one({'_id': ObjectId(new_author['_id'])})
    assert author is not None
    assert author['_id'] == new_author['_id']
