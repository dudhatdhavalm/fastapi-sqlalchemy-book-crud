from fastapi.encoders import jsonable_encoder
from unittest.mock import MagicMock, Mock
from app.crud.base import *

import pytest


from unittest.mock import MagicMock, Mock
from sqlalchemy.orm import Session
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import ObjectId

from unittest.mock import patch
from pymongo.collection import ReturnDocument
from unittest.mock import Mock, MagicMock
import pymongo
from bson.json_util import dumps



def test_update_obj_in_update_schema_type(
    crud_base_instance, model_instance, update_schema_type_instance, session_mock
):
    session_mock = MagicMock(spec=MongoClient)

    crud_base_instance.update(
        session_mock, db_obj=model_instance, obj_in=update_schema_type_instance
    )

    model_instance.dict.assert_called_once_with(exclude_unset=True)
    session_mock[crud_base_instance.collection_name].find_one_and_update.assert_called_once_with(
        {'_id': model_instance.dict(exclude_unset=True)["_id"]}, 
        {'$set': update_schema_type_instance.dict(exclude_unset=True)}, 
        return_document=True
    )
    json_data = dumps(model_instance.dict(exclude_unset=True))
    assert session_mock[crud_base_instance.collection_name].find_one(
        {'_id': model_instance.dict(exclude_unset=True)["_id"]}
    ) == json_data


def test_update_obj_in_dict(crud_base_instance, model_instance, session_mock):
    session_mock = MagicMock(spec=pymongo.collection.Collection)
    model_instance = Mock(spec=ObjectId)
    session_mock.find_one_and_update = MagicMock()

    id = ObjectId()
    obj_in = {"name": "Updated Test Book", "author": "Updated Test Author"}

    crud_base_instance.update(session_mock, db_obj=id, obj_in=obj_in)
    
    filter = {"_id": id}
    update = { "$set": obj_in }
    session_mock.find_one_and_update.assert_called_once_with(filter, update)


class UpdateSchemaType(BaseModel):
    name: str
    author: str


@pytest.fixture
def session_mock() -> Session:
    session = Mock(spec=Session)
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    return session



@pytest.fixture
def crud_base_instance() -> MongoDB:
    return MongoDB()


@pytest.fixture
def model_instance() -> dict:
    instance = {"_id": ObjectId(), "name": "Test Book", "author": "Test Author"}
    return instance


@pytest.fixture
def update_schema_type_instance() -> UpdateSchemaType:
    # Represents Mongo's _id in string form
    _id = "60fd1664684b18239caa8e22" # Placeholder. Use a valid id for your actual testing
    return UpdateSchemaType(_id, "Test Book", "Test Author")
