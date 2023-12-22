from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from app.crud.base import CRUDBase
from sqlalchemy import Column, Integer


from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
import pytest
from pymongo.collection import Collection

Base = declarative_base()


class FakeModel(Base):
    __tablename__ = "fake_table"
    id = Column(Integer, primary_key=True)


def test_crudbase_init(fake_model):
    instance = CRUDBase(collection=fake_model)
    assert (
        instance.collection is fake_model
    ), "Collection should be assigned to instance correctly"


@pytest.fixture
def fake_model():
    return FakeModel
