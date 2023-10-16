# Required imports
from typing import Type, TypeVar
from sqlalchemy.orm import Session


from typing import Type, TypeVar
from app.db.base_class import Base
from app.crud.base import *

import pytest
from app.crud.base import CRUDBase
from pymongo import MongoClient

ModelType = TypeVar("ModelType", bound=Base)


# Input mock
class MockModel(Base):
    pass


# Test that __init__ function in CRUDBase doesn't throw errors when it's executed
def test_CRUDBase_init_doesnt_throw_errors():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client.test_database
        collection = db.test_collection

        crud_base = CRUDBase(collection)
        
        assert crud_base is not None
        assert isinstance(crud_base.model, MongoClient)

    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

ModelType = TypeVar("ModelType", bound=Base)
