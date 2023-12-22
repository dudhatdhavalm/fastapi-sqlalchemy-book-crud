
from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from app.crud.base import CRUDBase
from sqlalchemy import Column, Integer


from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
import pytest

Base = declarative_base()


# Test Model to be used for the CRUDBase instance
class FakeModel(Base):
    __tablename__ = "fake_table"
    id = Column(Integer, primary_key=True)


# Test to ensure CRUDBase.__init__ does not throw errors and correctly assigns the model
def test_crudbase_init(fake_model):
    instance = CRUDBase(model=fake_model)
    assert (
        instance.model is fake_model
    ), "Model should be assigned to instance correctly"


# Fixture for the fake model
@pytest.fixture
def fake_model():
    return FakeModel
