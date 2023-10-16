import pytest
from app.crud.crud_author_plain import *
from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate


from datetime import date

import pytest
from app.crud.base import CRUDBase
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


def test_update_keep_old_value_if_not_in_dict():
    client = MongoClient()  # Connecting to the MongoDB
    db = client["some_database"]  # Use your database name
    authors = db["authors"]  # "authors" collection

    # Simulating the creation of an author
    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": datetime.utcnow(),
    }
    author_id = authors.insert_one(author_data).inserted_id

    # Update the author record
    update_data = {"email": "updated@example.com"}
    authors.update_one({"_id": ObjectId(author_id)}, {'$set': update_data})

    # Fetch the same document again
    updated_author = authors.find_one({"_id": ObjectId(author_id)})

    assert updated_author is not None
    assert updated_author["email"] == "updated@example.com"
    assert updated_author["name"] == "test_name"


def test_update_no_error():
    client = MongoClient()
    db = client["test_database"]
    author_collection = db["author"]
    
    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": date.today()
    }
    inserted_id = author_collection.insert_one(author_data).inserted_id
    
    update_data = {"$set": {"name": "updated_name"}}
    author_collection.update_one({"_id": inserted_id}, update_data)
    
    updated_author = author_collection.find_one({"_id": inserted_id})
    
    assert updated_author is not None
    assert updated_author['name'] == "updated_name"


def test_update_with_model_instance():
    client = MongoClient()
    db = client.test_database
    authors = db.authors

    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": datetime.now(),
    }

    # Insert a new author
    new_author_id = authors.insert_one(author_data).inserted_id

    # Update the author
    update_model = {"$set": {"name": "updated_name"}}
    authors.update_one({"_id": ObjectId(new_author_id)}, update_model)

    # Get the updated author
    updated_author = authors.find_one({"_id": ObjectId(new_author_id)})

    assert updated_author is not None
    assert updated_author['name'] == "updated_name"
