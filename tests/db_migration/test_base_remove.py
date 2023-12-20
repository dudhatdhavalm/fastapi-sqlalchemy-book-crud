
import pytest
from unittest.mock import MagicMock, patch
from app.crud.base import *
from app.crud.base import CRUDBase


class ExampleModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class TestCRUDBase:
    @patch("sqlalchemy.orm.Session")
    def test_remove(self, mock_session):
        # Given
        model_instance = ExampleModel(id=1, name="test")
        mock_session.query.return_value.get.return_value = model_instance

        # When
        crud = CRUDBase(model=ExampleModel)
        result = crud.remove(db=mock_session, id=1)

        # Then
        mock_session.delete.assert_called_once_with(model_instance)
        mock_session.commit.assert_called_once()
        assert result is model_instance
