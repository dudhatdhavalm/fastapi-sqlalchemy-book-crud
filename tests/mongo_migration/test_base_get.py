from sqlalchemy.orm import Session

import pytest
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from app.crud.base import *
from app.crud.base import CRUDBase
from mongoengine.queryset import QuerySet

ModelType = TypeVar("ModelType", bound=Base)




class TestCRUDBaseGet:

    @patch("mongoengine.queryset.QuerySet")
    def test_crudbase_get(self, mock_db):
        test_model = TypeVar("TestModel")
        mock_db.skip.return_value.limit.return_value.all.return_value = [
            test_model
        ]
        crud_base = CRUDBase(test_model)
        result = crud_base.get(db=mock_db, skip=0, limit=1)
        assert result is not None
