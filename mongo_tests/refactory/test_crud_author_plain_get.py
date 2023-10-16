from sqlalchemy.orm import Session
from typing import Any, Dict, List, Union
from fastapi.encoders import jsonable_encoder


from app.crud import CRUDAuthor
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from sqlalchemy import create_engine, engine, sessionmaker
from datetime import date

import pytest
from app.crud.crud_author_plain import *
import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
from app.crud import CRUDAuthorMongoDB
from typing import Optional


def test_get_invalid_id(db_session: MongoClient):
    author_crud = CRUDAuthor(db_session['test_db'])
    fetched_author = author_crud.get(100)
    assert (
        fetched_author is None
    ), f"function returned an author object for a non-existing id, expected None"


# Test Cases

def test_get(mongodb_session):
    author_crud = CRUDAuthorMongoDB()
    fetched_author = author_crud.get(mongodb_session, ObjectId("507f1f77bcf86cd799439011")) #pass a valid ObjectId
    assert fetched_author is not None, f"function returned None, expected Author object"
    assert isinstance(
        fetched_author, dict
    ), f"function returned {type(fetched_author).__name__}, expected dict (as MongoDB returns data in BSON format which is very similar to JSON)"


@pytest.fixture
def db_session():
    # Create session and add base test case
    client = MongoClient(f"mongodb+srv://<username>:<password>@cluster0.mongodb.net/BooksDB?retryWrites=true&w=majority")
    db = client.BooksDB_test
    base_author = AuthorCreate(name="Author name", date_of_birth=datetime(1990, 1, 1))
    base_author_id = db.author.insert_one(base_author.dict()).inserted_id
    yield db
    db.author.delete_one({'_id': ObjectId(base_author_id)})
    client.close()
