from sqlalchemy.engine import Engine


import pytest
from app.models.author import Author
from sqlalchemy import create_engine, inspect
from app.api.endpoints.author import *
from sqlalchemy import inspect
import pytest
from pymongo import MongoClient



@pytest.fixture
def engine():
    return MongoClient('mongodb://localhost:27017/')


@pytest.fixture
def author_table():
    client = MongoClient()
    database = client.test_database
    return database.author


def test_recreate_database(client: MongoClient):
    recreate_database()  # I assume this now recreates the "author" collection in MongoDB.
    
    db = client['your_database']  # replace 'your_database' with your actual db name.
    collection_names = db.list_collection_names()
    assert (
        "author" in collection_names
    ), f"'author' collection not found after running recreate_database()"
    
    author_collection = db['author']

    # Similarly, replace 'your_author_fields' with actual field names you're expecting in author collection.
    expected_field_names = set('your_author_fields')  # E.g. set(['_id', 'name', 'surname'])
    doc_sample = author_collection.find_one()
    
    if doc_sample is not None:
        actual_field_names = set(doc_sample.keys())
        assert (
            expected_field_names == actual_field_names
        ), "'author' collection does not match expected schema"
    else:
        assert (
            expected_field_names == set()
        ), "'author' collection does not match expected schema"
