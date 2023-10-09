from sqlalchemy import create_engine
from app.crud.crud_author import *
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Union
from app.models.author import Author

import pytest
from sqlalchemy.orm import clear_mappers, sessionmaker
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client.test_database
collection = db.test_collection


@pytest.fixture(scope="module")
def db():
    # Assuming connection string for your MongoDB
    client = MongoClient('mongodb://user:password@localhost:27017/BooksDB')
    return client['BooksDB']



@pytest.fixture(scope="module")
def crud_author(db_uri):
    client = MongoClient(db_uri)
    db = client.test_database  # your database name
    return CRUDAuthor(db)


def test_update(crud_author):
    # Arrange
    created_author = crud_author.create(
        obj_in={"name": "AuthorName", "book": "BookName"}
    )
    _id = str(created_author.inserted_id)
    update_obj = {"name": "AuthorNameUpdate", "book": "BookNameUpdate"}

    # Act
    updated_author = crud_author.update_one({'_id': ObjectId(_id)}, {'$set': update_obj})

    # Assert
    author_from_db = crud_author.find_one({'_id': ObjectId(_id)})
    assert author_from_db['name'] == "AuthorNameUpdate"
    assert author_from_db['book'] == "BookNameUpdate"
