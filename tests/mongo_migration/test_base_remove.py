import pytest
from unittest.mock import MagicMock, patch
from app.crud.base import *
from app.crud.base import CRUDBase
from pymongo import MongoClient, database
from unittest.mock import patch


class ExampleModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name




class TestCRUDBase:

    @patch("pymongo.database.Database")
    def test_remove(self, mock_db):
        model_instance = {"_id": "605c6a5d3956a3a3c5e4c6ad", "name": "test"}
        mock_db.ExampleModel.find_one.return_value = model_instance

        with patch.object(CRUDBase, 'model', return_value=ExampleModel), \
                patch.object(ExampleModel, 'objects'), \
                patch.object(ExampleModel.objects, 'get', return_value=model_instance):
            crud = CRUDBase(model=ExampleModel)
            result = crud.remove(db=mock_db, id=model_instance["_id"])
        
        mock_db.ExampleModel.delete_one.assert_called_once_with({'_id': model_instance["_id"]})
        assert result is model_instance
