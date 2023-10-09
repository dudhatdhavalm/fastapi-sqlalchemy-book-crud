from sqlalchemy import create_engine, sessionmaker
from unittest.mock import Mock
from app.crud.crud_author_plain import *

from app.models.author import Author
from typing import Union
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId



@pytest.fixture
def database():
    client = MongoClient("mongodb://username:password@localhost:27017/BooksDB")
    db = client['BooksDB']
    yield db
    client.close()


def test_update_dict(sample_author, database):
    crud_author = CRUDAuthor()

    updated_author = crud_author.update(
        db=database, db_obj=sample_author, obj_in={"name": "Updated author"}
    )


def test_update_object(sample_author, database):
    crud_author = CRUDAuthor()

    sample_author['name'] = "Updated author"
    updated_author_id = crud_author.update(database, sample_author['_id'], sample_author)

    updated_author = database.find_one({"_id": ObjectId(updated_author_id)})

    assert updated_author['name'] == "Updated author"


@pytest.fixture
def sample_author():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["test_database"]
    authors = db["authors"]

    author = {
        "_id": 1,
        "name": "Author",
        "dob": datetime(1990, 5, 5)
    }
    authors.insert_one(author)
    yield author

    # Clean up (delete the test author) after test run
    authors.delete_one({"_id": 1})
