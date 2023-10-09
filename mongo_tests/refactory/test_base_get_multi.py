from app.db.base_class import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from unittest.mock import MagicMock, patch
from app.crud.base import *


from unittest.mock import MagicMock, patch

import pytest
from pymongo import MongoClient
import pymongo
from bson import ObjectId


@pytest.fixture(scope="module")
def test_db():
    # Creating a new database on the fly
    # don't worry about cleaning it in the future
    client = MongoClient('mongodb://localhost:27017/')
    db = client['BooksDBTest']
    return db


@pytest.fixture
def crud_base_mock():
    with patch("app.CRUD_base.CRUD_base", autospec=True) as mock:
        yield mock


def test_get_multi_skip_limit(mocked_mongo_db, crud_base_mock):
    crud_base = crud_base_mock(model=MagicMock())

    # Execute query with skip and limit
    crud_base.get_multi(mocked_mongo_db, skip=0, limit=100)

    # Check if the methods skip and limit were called with appropriate values
    mocked_mongo_db.collection.skip.assert_called_with(0)
    mocked_mongo_db.collection.limit.assert_called_with(100)


def test_get_multi_no_skip_limit(mongodb, crud_base_mock):
    # creating a CRUD object with the mock model
    crud_base = crud_base_mock(collection_name=MagicMock())
    crud_base.get_multi(mongodb)

    # Check if the methods skip and limit were called with default values
    crud_base_mock.find().skip.assert_called_with(0)
    crud_base_mock.find().limit.assert_called_with(100)
