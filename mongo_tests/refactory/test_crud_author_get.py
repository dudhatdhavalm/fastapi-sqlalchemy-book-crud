from app.crud.crud_author import *
from fastapi.encoders import jsonable_encoder
from unittest.mock import MagicMock, Mock
from app.models.author import Author


from typing import Any, Dict, List, Union

import pytest
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from pymongo import MongoClient
from bson import ObjectId
from bson.objectid import ObjectId
from unittest.mock import MagicMock, patch
from pymongo.errors import DuplicateKeyError
from typings import Any, Dict, List, Union
from unittest.mock import patch


@patch('pymongo.collection.Collection.find_one')
def test_get_author_multiple_results(mock_find_one, db_session, crud_author):
    # Arrange
    test_author_id = 2
    multiple_authors = [
        {"id": test_author_id, "name": "test author1"},
        {"id": test_author_id, "name": "test author2"},
    ]

    mock_find_one.side_effect = DuplicateKeyError("duplicate key error collection: test.authors index: _id_ dup key: { : (2.0)}")

    # Act and assert
    with pytest.raises(DuplicateKeyError):
        crud_author.get(db_session, test_author_id)

    mock_find_one.assert_called_with({"_id": test_author_id})


def test_get_author_nonexistent(db_session, crud_author):
    # Arrange
    test_author_id = 999

    # Instead of query, in pymongo we work directly with the collections
    db_session.collection.find_one.return_value = None

    # Act
    result = crud_author.get(db_session, str(ObjectId(test_author_id)))

    # Assert
    # Pymongo's find_one operates on dictionaries
    db_session.collection.find_one.assert_called_with({"_id": ObjectId(test_author_id)})
    assert result is None


def test_get_author_existing(db_session, crud_author):
    # Arrange
    test_author_id = ObjectId()
    test_author = {"_id": test_author_id, "name": "test author"}
    db_session = MongoClient().db
    db_session['authors'].insert_one(test_author)
    crud_author = MagicMock()

    # Mocking find_one method
    with patch('pymongo.collection.Collection.find_one') as mock_find:
        mock_find.return_value = test_author

        # Act
        result = crud_author.get(db_session, test_author_id)

        # Assert
        mock_find.assert_called_with({"_id": test_author_id})
        assert result == test_author

    # Cleanup
    db_session['authors'].delete_one({"_id": test_author_id})


@pytest.fixture
def crud_author():
    client = MongoClient('localhost', 27017)
    db = client['mydatabase']
    author_collection = db['authors']
    return author_collection


@pytest.fixture
def db_session():
    return MockMongoClient()
