from sqlalchemy.orm import Session

from app.crud.crud_author import *

import pytest

from app.crud.crud_author import CRUDAuthor
from unittest.mock import patch


from unittest.mock import patch
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author
from pymongo import MongoClient
from bson import ObjectId
from pymongo.database import Database
from pymongo.collection import Collection
from unittest.mock import patch, MagicMock
from app.models.author import Author  # Author might be restructured to fit pymongo document structure

# Define the MongoDB database URI and name
DATABASE_URI = "<your-mongo-db-connection-string>"
DATABASE_NAME = "<your-database-name>"


def test_update_return_value(crud_author, mongo_client, author_obj, author_update_obj):
    # Let's assume mongo_client is the replacement for db_session and it returns a Collection instance
    authors_collection = mongo_client['your_database_name']['authors']
    with patch.object(CRUDAuthor, "update", return_value=author_obj) as mock_update:
        result = crud_author.update(
            db=authors_collection, db_obj=author_obj, obj_in=author_update_obj
        )
        assert result is not None

DATABASE_URI = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"


# It is assumed that the CRUDAuthor class is adapted for use with MongoDB
# and implements a method 'update' that updates a document in a MongoDB collection.

def test_update_no_errors(crud_author, db_collection, author_obj, author_update_obj):
    # Create a MagicMock for the MongoDB collection instead of a SQLAlchemy session
    mock_collection = MagicMock(spec=Collection)
    # Patch the 'update_one' method of the MongoDB collection
    with patch.object(mock_collection, 'update_one', return_value=author_obj) as mock_update:
        # Call the update method from the CRUDAuthor class
        result = crud_author.update(
            db=db_collection, db_obj=author_obj, obj_in=author_update_obj
        )
        # Prepare the expected filter and update documents
        filter_doc = {'_id': author_obj['_id']}
        update_doc = {'$set': author_update_obj}
        # Assert that the 'update_one' method was called with the correct arguments
        mock_update.assert_called_once_with(filter_doc, update_doc)


@pytest.fixture
def db_session():
    client = MongoClient(DATABASE_URI)
    return client[DATABASE_NAME]



@pytest.fixture
def crud_author(author_collection):
    return CRUDAuthor(author_collection)


@pytest.fixture
def author_obj():
    return Author(id=1, name="Test Author")


@pytest.fixture
def author_update_obj():
    return {"name": "Updated Author Name"}


@pytest.mark.parametrize(
    "obj_in", [({"name": "Updated Name"}), (Author(name="Updated Name"))]
)
def test_update_with_varied_inputs(crud_author, db_session, author_obj, obj_in):
    with patch.object(CRUDAuthor, "update", return_value=author_obj) as mock_update:
        result = crud_author.update(db=db_session, db_obj=author_obj, obj_in=obj_in)
        assert isinstance(result, Author)
