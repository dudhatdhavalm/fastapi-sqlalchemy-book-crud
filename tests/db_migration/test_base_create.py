from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy import Column, Integer, String, create_engine
import pytest
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel as PydanticBaseModel


import pytest

# Define the base class for SQLAlchemy models from the given file path
Base = declarative_base()

# Given file structure indicates app/crud/base.py contains the CRUDBase class
# Since CRUDBase is already in scope per the instructions, we do not need to import it.


# Simulate a dummy Pydantic schema for creation
class DummyCreateSchema(PydanticBaseModel):
    data: str
    created_by: Optional[str] = None


# Simulate a dummy SQLAlchemy model class with at least one primary key
class DummyModel(Base):
    __tablename__ = "dummy_model"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    created_by = Column(String, nullable=True)


# Test cases to verify that the method 'create' doesn't throw errors
def test_create_without_errors(db_session: Session):
    # In this test we want to verify that the function doesn't throw errors when it's executed
    obj_in = DummyCreateSchema(data="some_data", created_by="user1")
    db_obj = CRUDBase(DummyModel).create(
        db_session, obj_in=obj_in, created_by=obj_in.created_by
    )
    assert db_obj is not None, "The create method should return an object."


def test_create_with_none_created_by(db_session: Session):
    obj_in = DummyCreateSchema(data="some_data")
    db_obj = CRUDBase(DummyModel).create(db_session, obj_in=obj_in)
    assert db_obj.created_by is None, "created_by should be None when not provided."


# Fixture for providing a database session
@pytest.fixture(scope="module")
def db_session():
    # Setup the database URL
    DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Create tables for the dummy models
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a new database session for a test run
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)  # Optional: Clean up tables after tests run
