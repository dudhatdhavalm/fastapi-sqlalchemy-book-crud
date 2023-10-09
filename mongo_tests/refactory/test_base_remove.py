from typing import Generator
from app.db.base_class import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app.crud import CRUDBase
from sqlalchemy.orm import scoped_session, sessionmaker
from app.crud.base import *

from sqlalchemy import Column, Integer, String, create_engine
import pytest
from pymongo import MongoClient
from pymongo import MongoClient, collection
from pymongo.database import Database
from bson.objectid import ObjectId

DATABASE_URL = "postgresql://username:password@localhost:5432/BooksDB"
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(session_maker(bind=engine))


def test_remove(crud_base: CRUDBase, test_session: MongoClient):
    sample_model = {"value": "testing"}
    inserted_model = test_session.db.test.insert_one(sample_model)
    assert test_session.db.test.count_documents({}) == 1

    removed_model = crud_base.remove(test_session.db.test, id=inserted_model.inserted_id)

    assert removed_model is not None
    assert removed_model.deleted_count == 1
    assert test_session.db.test.count_documents({}) == 0


def test_remove_invalid_id(crud_base: CRUDBase, test_session: MongoClient):
    collection = test_session['test_db']['test_collection']
    initial_count = collection.count_documents({})
    with pytest.raises(Exception):
        crud_base.remove(test_session, id=999)
        final_count = collection.count_documents({})
        assert initial_count == final_count


class SampleModel(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, autoincrement=True)


@pytest.fixture(scope='function')
def test_session() -> Generator:
    """Generate a test session for integration tests."""
    test_client = MongoClient(
        "mongodb://username:password@localhost:27017/BooksDB_test"
    )
    test_db = test_client['BooksDB_test']
    yield test_db
    test_client.close()




@pytest.fixture(scope="module")
def crud_base() -> CRUDBase:
    client = MongoClient()
    db: Database = client['test_database']
    sample_collection: collection = db['sample_model']
    return CRUDBase(sample_collection)
