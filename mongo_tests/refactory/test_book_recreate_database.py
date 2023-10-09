from sqlalchemy import create_engine, inspect
from app.api.endpoints.book import *
from sqlalchemy import create_engine, inspect
from app.settings import DATABASE_URL
from app.models.book import Base
import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId




@pytest.fixture(scope="module")
def engine():
    return MongoClient(DATABASE_URL)


# import MongoClient from pymongo module. 

# Creating the metadata equivalent in pymongo 
# Since MongoDB doesn't have a similar concept to a metadata we are returning the database instance instead.
@pytest.fixture(scope="module")
def metadata():
    client = MongoClient(DATABASE_URL)
    db = client.get_database()

    return db


def test_recreate_database(engine, metadata):
    # Connect to MongoDB
    client = MongoClient(DATABASE_URL)
    # Ensure that the BooksDB is empty before the test
    booksdb = client['BooksDB']
    assert 'BooksDB' not in client.list_database_names()

    # Call target function
    recreate_database()

    # Check that the BooksDB has been created
    assert 'BooksDB' in client.list_database_names()  
