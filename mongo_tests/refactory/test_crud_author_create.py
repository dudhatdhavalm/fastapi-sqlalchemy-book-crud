import pytest
from sqlalchemy.orm import Session
from app.crud.crud_author import *
from app.models.author import Author


import pytest
from app.schemas.author import AuthorCreate
from app.crud.crud_author import CRUDAuthor
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo


def teardown_function(function):
    print(f"tearing down {function}")
    # Creating a client object
    client = MongoClient('mongodb://localhost:27017')
    # Assuming you have a database named 'mydb'
    mydb = client['mydb']
    # Assuming 'mycollection' is the collection of 'mydb'
    mycollection = mydb['mycollection']
    # Clearing all the documents in the collection
    mycollection.delete_many({})


def setup_function(function):
    print(f"setting up {function}")
    # Initial setup for the function. Create a new MongoClient instance, or maybe a test database?
    client = MongoClient("mongodb://localhost:27017")
    db = client["test_database"]

# As we cannot create a session in pymongo, we have to create a connection with MongoClient
db = MongoClient()['test']



def test_create():
    # Testing for normal input values
    name = "Test Author"
    CRUDAuthor_obj = CRUDAuthor()
    assert (
        CRUDAuthor_obj.create(obj_in=Author(name=name)) is not None
    )

    # Testing for empty input
    name = ""
    CRUDAuthor_obj = CRUDAuthor()
    assert (
        CRUDAuthor_obj.create(obj_in=Author(name=name)) is not None
    )

    # Test to handle invalid type inputs that create MongoDB driver errors
    with pytest.raises(Exception):
        name = 1234  # given name as integer, should raise an Exception
        CRUDAuthor_obj = CRUDAuthor()
        CRUDAuthor_obj.create(obj_in=name)
