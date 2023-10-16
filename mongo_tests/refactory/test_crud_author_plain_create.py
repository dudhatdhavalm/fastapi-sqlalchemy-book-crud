from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.models.author import Author


import pytest
from app.schemas.author import AuthorCreate
from datetime import date

import pytest
from app.crud.crud_author_plain import *
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from bson import ObjectId

from app.crud.crud_author_mongo import *
from pymongo.collection import Collection
import pymongo


def test_create_method_birth_field(mongo_db, author_create):
    mongo_db = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mongo_db["mydatabase"]
    mycol = mydb["author"]
    crud_author = CRUDAuthor()

    response = crud_author.create(db=mongo_db, obj_in=author_create)

    _id = response.inserted_id
    find_document = mycol.find_one({'_id': ObjectId(_id)})

    assert find_document['birth'] == datetime.today()


# assuming you have a mongo db running with database testdb and author collection.
# And author_create is a dictionary with structure like: {"name": "Test Name", "birth": "...", ...}

def test_create_method_name_field(client: MongoClient, author_create: dict):
    db = client["testdb"]
    collection = db["author"]
    response = collection.insert_one(author_create)
    assert response.inserted_id is not None
    inserted_author = collection.find_one({"_id": ObjectId(response.inserted_id)})
    assert inserted_author["name"] == "Test Name"


def test_create_method_return_type(client, author_create):
    crud_author = CRUDAuthor()
    response = crud_author.create(client=client, doc_in=author_create)
    assert isinstance(response.inserted_id, ObjectId)



def test_create_method_no_throws(session, author_create):
    crud_author = CRUDAuthor()
    response = None
    try:
        response = crud_author.create(db=session, obj_in=author_create)
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected error: {e}")

    assert response is not None


@pytest.fixture
def author_create() -> dict:
    return {"name": "Test Name", "birth": datetime.utcnow()}



@pytest.fixture
def session() -> MongoClient:
    return MongoClient()

def setup_module(module):
    global connection
    global db
    connection = MongoClient()
    db = connection.test_database

def teardown_module(module):
    connection.drop_database('test_database')
