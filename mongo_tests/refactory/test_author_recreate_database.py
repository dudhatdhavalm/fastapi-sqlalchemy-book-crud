import pytest
from app.models.author import Base


import pytest
from app.api.endpoints.author import *
from sqlalchemy import create_engine, text
from sqlalchemy import text
from pymongo import MongoClient


@pytest.fixture(scope="module")
def engine():
    DATABASE_URL = "mongodb://localhost:27017/"
    client = MongoClient(DATABASE_URL)
    return client['BooksDB']


@pytest.fixture(scope="module")
def connection():
    client = MongoClient()
    return client['test_database']



@pytest.fixture(scope="module")
def transaction(connection):
    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    yield
    client.drop_database('test_database')


@pytest.mark.usefixtures("transaction")
def test_recreate_database(engine, connection):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    
    # Recreate the database
    db.author.drop()
    db.book.drop()

    # Recreate collections
    db.create_collection("author")
    db.create_collection("book")

    # Check if collections are created
    collections = db.list_collection_names()
    assert "author" in collections
    assert "book" in collections



@pytest.mark.usefixtures("transaction")
def test_recreate_database_no_errors():
    def recreate_database():
        client = MongoClient("mongodb://localhost:27017/")
        db = client["your_database"]
        db.command("dropDatabase")

    # The 'recreate_database' function is called within the test function
    # so that the MongoDB database can be recreated (dropped first then recreated)
    # however you need to set this function as per your project's needs.
    assert recreate_database() is None
