from sqlalchemy.orm import Session

import pytest
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from app.crud.base import *
from app.crud.base import CRUDBase

ModelType = TypeVar("ModelType", bound=Base)


class TestCRUDBaseGet:
    @patch("sqlalchemy.orm.Session")
    def test_crudbase_get(self, mock_db):
        test_model = TypeVar("TestModel", bound=Base)
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [
            test_model
        ]
        crud_base = CRUDBase(test_model)
        result = crud_base.get(db=mock_db, skip=0, limit=1)
        assert result is not None
