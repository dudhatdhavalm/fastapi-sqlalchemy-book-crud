from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate

import pytest

from app.crud.crud_author import CRUDAuthor
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author
from unittest.mock import MagicMock, create_autospec

from app.crud.crud_author import *



from unittest.mock import MagicMock, create_autospec
from pymongo.collection import Collection
from bson.objectid import ObjectId
from bson import ObjectId  # This is used for MongoDB '_id' fields
from unittest.mock import MagicMock


# Fixture to set up CRUDAuthorMongo instance
@pytest.fixture(scope="module")
def crud_author_instance(db_session):
    # Simulate the collection object that would be returned by PyMongo
    mocked_collection = create_autospec(Collection, instance=True)
    
    return CRUDAuthorMongo(mocked_collection)


# We assume that the CRUDAuthor class methods have been modified to use PyMongo

def test_create_no_errors(crud_author_instance, db_session, author_create_data):
    """
    Test whether the 'create' method of CRUDAuthor class can be called without errors and returns a non-None result.
    MongoDB automatically generates the '_id' field, so we don't need to handle this part.
    """
    assert isinstance(db_session, Collection), "db_session should be an instance of pymongo.collection.Collection"

    # Creating a MagicMock for the insert_one method, which is the PyMongo way to add a document to the collection
    db_session.insert_one = MagicMock(return_value=None)

    # In PyMongo, when you insert a document, instead of None, you get an InsertOneResult instance
    # We can just mock this to have an 'inserted_id' attribute for testing purposes
    mocked_insert_result = MagicMock()
    mocked_insert_result.inserted_id = "mocked_id"
    db_session.insert_one.return_value = mocked_insert_result

    response = crud_author_instance.create(db=db_session, obj_in=author_create_data)

    # We check that insert_one has been called once
    db_session.insert_one.assert_called_once()

    # In a real scenario, response would be the inserted document with an _id field assigned by MongoDB
    # Since we are mocking, we'll just check for a non-None response
    assert response is not None



@pytest.fixture(scope="module")
def mock_author_instance():
    # We use an ObjectId to simulate an actual MongoDB _id.
    # Name and book properties remain the same.
    author = create_autospec(AuthorDocument, instance=True)
    author._id = ObjectId()
    author.name = "Jane Austen"
    author.book = "Pride and Prejudice"
    return author


@pytest.fixture(scope="module")
def db_session():
    return create_autospec(Session, instance=True)


@pytest.fixture(scope="module")
def author_create_data():
    return AuthorCreate(name="Jane Austen", book="Pride and Prejudice")

@pytest.fixture(scope="function")
def mongo_collection(mocker):
    # Mock MongoDB collection
    collection_mock = mocker.MagicMock(spec=Collection)
    return collection_mock
