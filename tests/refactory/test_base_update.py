from fastapi.encoders import jsonable_encoder
from unittest.mock import MagicMock, Mock
from app.crud.base import *

import pytest


from unittest.mock import MagicMock, Mock
from sqlalchemy.orm import Session
from pydantic import BaseModel


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
def update_schema_type_instance() -> UpdateSchemaType:
    return UpdateSchemaType(name="Test Book", author="Test Author")


@pytest.fixture
def crud_base_instance() -> CRUDBase:
    return CRUDBase(ModelType)


@pytest.fixture
def model_instance() -> ModelType:
    instance = Mock(spec=ModelType)
    instance.dict = MagicMock(
        return_value={"name": "Test Book", "author": "Test Author"}
    )
    return instance


def test_update_obj_in_dict(crud_base_instance, model_instance, session_mock):
    obj_in = {"name": "Updated Test Book", "author": "Updated Test Author"}
    crud_base_instance.update(session_mock, db_obj=model_instance, obj_in=obj_in)
    model_instance.dict.assert_not_called()
    session_mock.add.assert_called_once_with(model_instance)
    session_mock.commit.assert_called_once()
    session_mock.refresh.assert_called_once_with(model_instance)


def test_update_obj_in_update_schema_type(
    crud_base_instance, model_instance, update_schema_type_instance, session_mock
):
    crud_base_instance.update(
        session_mock, db_obj=model_instance, obj_in=update_schema_type_instance
    )
    model_instance.dict.assert_called_once_with(exclude_unset=True)
    session_mock.add.assert_called_once_with(model_instance)
    session_mock.commit.assert_called_once()
    session_mock.refresh.assert_called_once_with(model_instance)
