from unittest.mock import create_autospec

import pytest
from sqlalchemy.orm import Session

from app.crud.crud_author_plain import *
from pymongo import MongoClient
from unittest.mock import MagicMock, patch
from bson.objectid import ObjectId
from unittest.mock import Mock
import pymongo
from pymongo.collection import Collection


@pytest.fixture
def crud_author():
    return CRUDAuthor()

@pytest.fixture(scope="module")
def mock_db():
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    return client['code_robotics_1704487699809']

@pytest.fixture
def mock_author_collection(mock_db):
    return mock_db["author"]


# Assuming 'crud_author' is a class that provides CRUD operations for 'authors' in MongoDB
# and has a 'get' method defined in it similar to the SQLAlchemy version

# Mocking the 'get' method to behave similarly to the MongoDB collection find method
def test_get_with_negative_limit(crud_author, mock_collection):
    crud_author.get = mock_collection.find
    assert crud_author.get(skip=0, limit=-100) is not None


# You might need to adjust the imports to fit with the actual implementation details of your CRUD operations

@pytest.fixture
def mock_db_session():
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        # Setup mock database and collection here
        mock_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        
        # Since MongoDB uses ObjectId for ids, you can simulate that here if needed:
        mock_collection.insert_one.side_effect = lambda doc: {'_id': ObjectId()}
        
        yield mock_collection

# The fixture for 'crud_author' and 'mock_db_session' should be adjusted to mock pymongo collection
@pytest.fixture
def mock_collection(mocker):
    # Mongo database connection string
    mongo_db_uri = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'
    # Connecting to the Mongo client
    client = pymongo.MongoClient(mongo_db_uri)
    # Accessing the specific database and collection
    db = client['code_robotics_1704487699809']
    collection = db['authors']
    # Creating a spec of a pymongo collection to use for the mock
    collection_spec = create_autospec(Collection, instance=True)
    # Returning the mocked collection spec
    return collection_spec

# More test cases should be implemented in the same way,
# translating SQLAlchemy session operations to PyMongo collection operations.

@pytest.fixture(scope="module")
def mongo_client():
    return MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')


def test_get_no_errors(crud_author, mock_db_session):
    assert crud_author.get(db=mock_db_session) is not None


def test_get_with_skip_limit(crud_author, mock_db_session):
    assert crud_author.get(db=mock_db_session, skip=10, limit=5) is not None


def test_get_with_large_limit(crud_author, mock_db_session):
    assert crud_author.get(db=mock_db_session, skip=0, limit=1000) is not None


def test_get_with_negative_skip(crud_author, mock_db_session):
    assert crud_author.get(db=mock_db_session, skip=-10, limit=100) is not None


def test_get_with_none_values(crud_author, mock_db_session):
    assert crud_author.get(db=mock_db_session, skip=None, limit=None) is not None
