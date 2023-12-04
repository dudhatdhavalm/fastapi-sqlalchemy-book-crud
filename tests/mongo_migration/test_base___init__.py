from sqlalchemy import Column, Integer, String
from app.crud.base import *
import pytest
from pymongo import MongoClient


class MockModel(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))


def test_crudbase_init():
    """Test the __init__ method in the CRUDBase Class"""
    
    client = MongoClient('localhost', 27017)
    db = client['my_database']
    MockModel = db['my_collection']

    crud_base = CRUDBase(MockModel)
    assert crud_base is not None
    assert isinstance(crud_base, CRUDBase)
    assert crud_base.model == MockModel
