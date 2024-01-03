from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate

import pytest
import pytest

from app.crud.crud_author_plain import *

from app.models.author import Author  # Import corrected based on file structure


from unittest.mock import MagicMock, patch



from unittest.mock import MagicMock, patch
from bson import ObjectId

from app.models.author import Author  # Assuming this class now represents a MongoDB document
from app.crud.crud_author import CRUDAuthor  # Assuming you have CRUD operations for PyMongo
from pymongo.collection import Collection

from bson.objectid import ObjectId

from app.crud.crud_author_plain import AuthorCRUD  # Adjust the import according to your app structure
from app.crud.crud_author import CRUDAuthor  # You should define this file and class to interact with MongoDB
from your_application.crud_author_pymongo import CRUDAuthor
from unittest.mock import MagicMock


def test_update_changes_data(
    crud_author_instance, db_session_mock, author_db_obj, author_update_data
):
    # Assuming author_db_obj['_id'] is already set and is an instance of ObjectId
    db_session_mock.find_one_and_update.return_value = {**author_db_obj, **author_update_data}
    
    author_updated = crud_author_instance.update(
        db=db_session_mock, db_obj=author_db_obj, obj_in=author_update_data
    )
    
    db_session_mock.find_one_and_update.assert_called_with(
        {"_id": author_db_obj['_id']},
        {"$set": author_update_data},
        return_document=True
    )
    
    assert (
        author_updated['name'] == "Updated Author Name"
    ), "Author name was not updated correctly"


# Define a test case function for pymongo
def test_update_no_errors(crud_author_instance, author_db_obj, author_update_data):
    db_session_mock = MagicMock()  # Simulate a PyMongo database collection

    # Given an author object with an "_id"
    author_db_obj_id = ObjectId()
    author_db_obj["_id"] = author_db_obj_id

    # Instantiate the CRUD object with the mocked session
    crud_author_instance = CRUDAuthor(db_session_mock)

    try:
        # Call the update function using pymongo syntax
        result = crud_author_instance.update(
            author_id=author_db_obj_id, obj_in=author_update_data
        )
        assert result.modified_count == 1
    except Exception as e:
        pytest.fail(f"Update method raised an error unexpectedly: {e}")


@pytest.fixture
def crud_author_instance():
    return CRUDAuthor()


# Let's assume AuthorCRUD contains PyMongo implementation

# PyMongo often uses 'collection', here we mock the collection instead of sqlalchemy.orm.Session
# The fixture's name is kept the same for compatibility with your tests
@pytest.fixture
def db_session_mock():
    with patch("pymongo.collection.Collection") as mock_collection:
        # PyMongo's insert_one method returns an InsertOneResult with inserted_id attribute
        mock_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId())
        # You'll need to set up appropriate return values for other collection methods (e.g., find_one, update_one)
        yield mock_collection


# Assuming collection is already set up and ready to be used for testing
# Example: collection = MongoClient().db.author_collection

@pytest.fixture
def author_update_data():
    return {"name": "Updated Author Name"}



@pytest.fixture
def author_db_obj():
    # In MongoDB, the primary key field is _id and is an ObjectId.
    return Author(_id=ObjectId(), name="Existing Author")


@pytest.fixture
def author():
    # MongoDB uses '_id' instead of 'id', and it's auto-generated as an ObjectId.
    # We can mock this for our tests or just call ObjectId() to generate one.
    return Author(name="Example Author")

@pytest.fixture
def db_collection_mock():
    # Mock the pymongo collection
    return MagicMock()


def test_update_ignores_unexpected_fields(
    crud_author_instance, db_session_mock, author_db_obj
):
    unexpected_data = {"unexpected_field": "some value"}
    author_original_name = author_db_obj.name
    crud_author_instance.update(
        db=db_session_mock, db_obj=author_db_obj, obj_in=unexpected_data
    )
    assert (
        author_db_obj.name == author_original_name
    ), "Author name should not have changed"

