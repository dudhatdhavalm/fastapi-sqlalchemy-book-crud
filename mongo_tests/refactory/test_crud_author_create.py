from app.crud.crud_author import *
from app.crud.crud_author import CRUDAuthor
from unittest.mock import Mock, patch
from app.models.author import Author

import pytest
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from unittest.mock import Mock


# Assuming CRUDAuthor is a class to handle CRUD operations on Author collection
# And it has a method called 'create' to insert new author data

def test_create_with_faulty_data(setup_faulty_data):
    client = Mock(spec=MongoClient)
    author_crud = CRUDAuthor()

    with pytest.raises(Exception):
        author_crud.create(client, obj_in=setup_faulty_data)



@pytest.fixture
def setup_faulty_data():
    return {"_id": ObjectId(), "name": "John Doe"}


@patch(
    "app.crud.crud_author.jsonable_encoder", return_value={"_id": 1, "name": "John Doe"}
)
@patch("pymongo.collection.Collection.insert_one")
@pytest.mark.parametrize(
    "author_input",
    [
        ({"_id": 1, "name": "John Doe"}),
        ({"_id": 2, "name": "Jane Doe"}),
    ],
)
def test_create(mock_add, mock_jsonable_encoder, author_input):
    collection = Mock(spec=Collection)
    author_crud = CRUDAuthor()
    author_schema = AuthorCreate(**author_input)

    result = author_crud.create(collection, obj_in=author_schema)

    mock_jsonable_encoder.assert_called_once_with(author_schema)
    mock_add.assert_called_once_with(author_input)
    assert isinstance(result, dict)
    assert result['_id'] == author_input["_id"]
    assert result['name'] == author_input["name"]
