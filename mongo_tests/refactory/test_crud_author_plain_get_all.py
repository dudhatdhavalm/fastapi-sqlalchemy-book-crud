from datetime import date
from app.crud.crud_author_plain import *

from app.models.author import Author
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime



def test_get_all_empty(db_session):
    client = MongoClient('localhost', 27017)
    db = client['test_database']
    collection = db['authors']

    crud_author = CRUDAuthor()
    result = crud_author.get_all(collection)
    assert isinstance(result, list)
    assert len(result) == 0


def test_get_all_with_data(mongodb_session, sample_author):
    authors = mongodb_session.db.authors
    result = authors.insert_one(sample_author)
    inserted_id = result.inserted_id
    crud_author = CRUDAuthor()
    result = crud_author.get_all(mongodb_session)
    assert isinstance(result, list)
    assert len(result) == 1
    author = result[0]
    assert author['_id'] == ObjectId(inserted_id)
    assert author['name'] == "John Doe"
    assert author['birth_date'] == datetime(2000, 1, 1)


def test_get_all_with_skip_limit():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['db_test']
    collection = db['authors']

    for i in range(5):
        author = { "_id": i, "name": f"Author {i}", "birth_date": "2000-01-01"}
        collection.insert_one(author)

    authors = collection.find().skip(1).limit(2)
    result = [author for author in authors]
    
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]['_id'] == 1
    assert result[1]['_id'] == 2

    authors = collection.find().skip(3).limit(1)
    result = [author for author in authors]
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['_id'] == 3


@pytest.fixture
def db_session():
    client = MongoClient('localhost', 27017)
    db = client['mydatabase']
    yield db
    client.close()


@pytest.fixture
def sample_author():
    return {"_id": ObjectId(),
            "name": "John Doe",
            "birth_date": datetime(2000, 1, 1)}
