from app.db.base_class import Base
from unittest.mock import MagicMock, patch
from app.crud.base import *

import pytest
from sqlalchemy.orm import Session


# Define a fake Model inherited from Base
class FakeModel(Base):
    def __init__(self, id):
        self.id = id


class TestCRUDBase:
    @pytest.fixture
    def fake_db(self):
        # Create a fake db session
        db = MagicMock(spec=Session)
        db.query().filter().first.return_value = None
        return db

    @patch("app.db.base_class.Base", new_callable=FakeModel)
    def test_get(self, fake_db):
        crud_base = CRUDBase(FakeModel)

        assert crud_base.get(fake_db, 1) == None

        fake_db.query().filter().first.assert_called_once_with()

    @patch("app.db.base_class.Base", new_callable=FakeModel)
    def test_get_with_model(self, fake_db):
        instance = FakeModel(1)

        # Update the return value of the first method
        fake_db.query().filter().first.return_value = instance

        crud_base = CRUDBase(FakeModel)

        assert crud_base.get(fake_db, 1) == instance

        fake_db.query().filter().first.assert_called_once_with()
