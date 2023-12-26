from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.crud.crud_author_plain import *

import pytest
from unittest.mock import MagicMock, patch

from app.crud.crud_author_plain import CRUDAuthor
from app.models.author import Author
from sqlalchemy.orm import Session




from unittest.mock import MagicMock
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId



@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


# Assuming the mocks return appropriate PyMongo-like mocked objects this time
# db_session in the context of PyMongo would refer to a mocked Collection object
# db_obj would be a dictionary representing the MongoDB document with an '_id' field
# update_data_dict would be the dictionary with fields to be updated 

def test_update_no_errors(db_session, db_obj, update_data_dict):
    crud_author = CRUDAuthor()

    # Assuming update method expects a MongoDB Collection object (or a Mock of it),
    # a document (Mock or Dict with '_id'), and a dictionary of the fields to update.
    # In PyMongo, updates would use the '_id' field to find the document.
    _id = db_obj.get('_id')

    # The update should use a {"$set": update_data_dict} to perform a partial update
    # of the fields given by update_data_dict.
    # For testing, you need to ensure that the mock for db_session's update_one method
    # is set up to simulate a PyMongo operation correctly.
    with patch.object(Collection, 'update_one') as mock_update_one:
        crud_author.update(db_session, db_obj=db_obj, obj_in=update_data_dict)
        mock_update_one.assert_called_once_with({'_id': _id}, {'$set': update_data_dict})


@pytest.fixture
def db_obj():
    author = Author()
    author.id = 1
    author.name = "Original Author"
    return author


@pytest.fixture
def update_data_dict():
    return {"name": "Updated Author"}


# Make sure to install pymongo if not already installed
# pip install pymongo

@pytest.fixture
def update_data_author():
    # In pymongo, data is represented as dictionaries
    # MongoDB uses "_id" for the primary key, not "id"
    return {'_id': ObjectId(), 'name': 'Updated Author'}
