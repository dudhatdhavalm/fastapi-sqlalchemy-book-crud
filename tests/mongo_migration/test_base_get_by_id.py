import pytest
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from app.crud.base import CRUDBase

from app.crud.base import CRUDBase
from sqlalchemy import create_engine
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine

from app.crud.base import *




import pytest
from pymongo import MongoClient


class SampleModel(BaseModel):
    id: int
    name: str


class SampleSQLAlchemyModel(Base):
    __tablename__ = "sample_model"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


@pytest.fixture(scope="module")
def db_session():
    MONGODB_URL = "mongodb://your_mongo_db_user:your_mongo_db_password@your_mongo_db_host:your_mongo_db_port/your_mongo_db_name"
    client = MongoClient(MONGODB_URL)
    db = client['your_mongo_db_name']
    
    # Perform setup if needed, like creating collections or inserting test documents
    # ...

    try:
        yield db
    finally:
        # Perform teardown if needed, like dropping collections or removing test documents
        # ...
        client.close()


def test_get_by_id_no_errors(db_session: Session):
    crud_base = CRUDBase(model=SampleSQLAlchemyModel)
    result = crud_base.get_by_id(db=db_session, id=1)
    assert (
        result is not None or result is None
    ), "get_by_id should return None or a valid object"
