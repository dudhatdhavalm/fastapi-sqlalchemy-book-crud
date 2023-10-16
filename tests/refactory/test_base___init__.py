# Required imports
from typing import Type, TypeVar
from sqlalchemy.orm import Session


from typing import Type, TypeVar
from app.db.base_class import Base
from app.crud.base import *

import pytest
from app.crud.base import CRUDBase

ModelType = TypeVar("ModelType", bound=Base)


# Input mock
class MockModel(Base):
    pass


# Test that __init__ function in CRUDBase doesn't throw errors when it's executed
def test_CRUDBase_init_doesnt_throw_errors():
    try:
        crud_base = CRUDBase(MockModel)
        assert crud_base is not None
        assert isinstance(crud_base.model, Type[Base])

    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")

ModelType = TypeVar("ModelType", bound=Base)
