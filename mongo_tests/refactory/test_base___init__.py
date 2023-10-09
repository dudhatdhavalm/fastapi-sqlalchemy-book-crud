

from app.crud.base import CRUDBase
from app.crud.base import *
import pytest


def test_crud_base_init():
    class ModelType:
        pass

    crud_base = CRUDBase(ModelType)
    assert crud_base.model == ModelType
