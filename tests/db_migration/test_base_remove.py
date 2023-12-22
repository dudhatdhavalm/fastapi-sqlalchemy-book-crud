from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, MetaData, String, create_engine


import pytest
import pytest

# Constants for test database connection
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DummyModel to mock real database model with a primary key
class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


# Setup the database, create dummy table and yield db session
@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def crud_base_instance(db_session):
    # Initialize the CRUD instance with the DummyModel
    instance = CRUDBase(DummyModel)
    yield instance


def test_remove_no_errors(db_session, crud_base_instance):
    # Add a dummy object to the session
    obj = DummyModel()
    db_session.add(obj)
    db_session.commit()

    # Ensure that the object is in the database
    assert db_session.query(DummyModel).get(obj.id) is not None

    # Test remove method
    deleted_obj = crud_base_instance.remove(db_session, id=obj.id)
    assert deleted_obj is not None, "Remove method should return the deleted object"

    # Check that the object is no longer in the session
    assert (
        db_session.query(DummyModel).get(obj.id) is None
    ), "Object should be deleted from the session"

# Necessary imports for the test suite
from sqlalchemy import Column, Integer, MetaData, create_engine
