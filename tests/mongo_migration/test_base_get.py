import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base


import pytest
from pymongo import MongoClient
from pymongo.collection import Collection

# Assuming a local MongoDB instance; update with your MongoDB URI as needed
MONGO_URI = "mongodb://localhost:27017/"

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


@pytest.fixture(scope="function")
def db_session():
    client = MongoClient(MONGO_URI)
    # Assuming the test database is named 'test_database'
    db = client['test_database']
    # Assuming DummyModel translates to a collection named 'dummy_model'
    dummy_model_collection = db['dummy_model']
    # Clean up the collection before each test
    dummy_model_collection.delete_many({})
    try:
        yield dummy_model_collection  # This replaces the 'db' session object
    finally:
        # Optionally, drop the collection after the test
        dummy_model_collection.drop()
        client.close()


@pytest.fixture(scope="function")
def crud_base(db_session: Session):
    return CRUDBase(DummyModel)


def test_get_no_errors(crud_base, db_session):
    assert crud_base.get(db_session) is not None


def test_get_limit_parameter(crud_base, db_session):
    assert len(crud_base.get(db_session, limit=10)) <= 10


def test_get_skip_parameter(crud_base, db_session):
    all_data = crud_base.get(db_session, limit=10)
    skipped_data = crud_base.get(db_session, skip=5, limit=5)
    assert all_data[5:] == skipped_data
