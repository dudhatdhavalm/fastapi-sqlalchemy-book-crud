from app.schemas.author import AuthorCreate
from app.models.author import Author

import pytest
from unittest.mock import Mock

from app.crud.crud_author_plain import *
from datetime import date
from sqlalchemy.orm import Session


from unittest.mock import Mock

import pytest

from app.models.author import Author
from pymongo.collection import Collection
from bson.objectid import ObjectId
from bson import ObjectId
from app.crud.crud_author_pymongo import CRUDAuthor
from unittest.mock import MagicMock
from app.crud.crud_author_mongo import CRUDAuthor # This is a modified version for MongoDB


def test_create_persists_object(mongo_collection: Collection, author_create_data: AuthorCreate):
    """Test that the create function successfully persists an object."""
    crud_author = CRUDAuthor()

    # Mocking insert_one and find_one methods from the PyMongo collection to simulate a MongoDB operation
    mongo_collection.insert_one = MagicMock(return_value={"inserted_id": "someMongoDbId"})
    mongo_collection.find_one = MagicMock()

    # The create method takes a PyMongo collection and JSON serializable dict - converting 'author_create_data' accordingly
    created_author = crud_author.create(db=mongo_collection, obj_in=author_create_data.dict())

    # Verifying that insert_one is called once and the appropriate object is persisted to MongoDB
    mongo_collection.insert_one.assert_called_once_with(author_create_data.dict())

    # The CRUDAuthor create method should return the inserted document including the generated _id 
    # - Verifying the 'find_one' is called to retrieve the inserted document
    # This assumes that the 'find_one' is used in the CRUDAuthor create method to retrieve the inserted document after creation
    mongo_collection.find_one.assert_called_once_with({"_id": created_author.inserted_id})


# Assuming that author_instance should contain a dictionary that represents an Author
def test_create_return_value(db_collection, author_create_data: AuthorCreate, author_instance: dict):
    """Test that the create function returns an Author instance."""
    crud_author = CRUDAuthor(collection=db_collection)
    db_collection.insert_one = MagicMock(return_value=author_instance)  # Simulate insertion

    result = crud_author.create(obj_in=author_create_data)
    assert isinstance(result, Author)


def test_create_no_exceptions(
    mongo_collection, author_create_data: dict, author_instance: dict
):
    """Test that the create function doesn't throw exceptions."""
    crud_author = CRUDAuthor()
    mongo_collection.insert_one = Mock(return_value={'inserted_id': author_instance['_id']})

    result = crud_author.create(db=mongo_collection, obj_in=author_create_data)
    assert result is not None
    mongo_collection.insert_one.assert_called_with(author_create_data)



@pytest.fixture
def author_instance() -> Author:
    """Fixture for generating Author sample data."""
    author = Mock(spec=Author)
    author._id = ObjectId()
    author.name = "Jane Doe"
    author.birth_date = date(1985, 5, 23)
    return author


@pytest.fixture
def db_session() -> Session:
    """Fixture for creating a mock database session."""
    return Mock(spec=Session)



@pytest.fixture
def author_create_data() -> dict:
    """Fixture for generating author create sample data in dictionary format."""
    # Convert AuthorCreate to the dictionary representation expected by pymongo
    return {"name": "Jane Doe", "birth_date": date(1985, 5, 23)}


@pytest.fixture
def db_collection(mocker) -> Collection:
    """Fixture to mock a MongoDB collection."""
    # Use the mocker fixture from pytest-mock to create a mock of a pymongo collection
    return mocker.Mock(spec=Collection)
