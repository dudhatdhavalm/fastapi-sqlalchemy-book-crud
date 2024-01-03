from sqlalchemy.orm import sessionmaker

from app.crud.base import *

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, String, create_engine


from typing import Optional
from pydantic import BaseModel
from typing import Any, Dict, Type, Union
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy base model for testing
Base = declarative_base()


# Define a dummy SQLAlchemy model class for testing with a primary key
class DummyModel(Base):
    __tablename__ = "dummy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    modified_by = Column(String)


# Define a dummy Pydantic BaseModel for testing
class UpdateSchema(BaseModel):
    name: str
    modified_by: Optional[str] = None


# Setup database connection and session for testing
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Instantiate a CRUDBase object with DummyModel
crud_base = CRUDBase(model=DummyModel)


# The first test checks if the function doesn't throw errors when executed.
def test_update_no_errors(db_session):
    # Creating a dummy entry for the test
    dummy_db_obj = DummyModel(name="Old Name")
    db_session.add(dummy_db_obj)
    db_session.commit()

    # Attempting to update the entry
    dummy_update_obj = {"name": "New Name", "modified_by": "Updater"}
    updated_obj = crud_base.update(
        db_session, db_obj=dummy_db_obj, obj_in=dummy_update_obj
    )

    assert (
        updated_obj is not None
    )  # The update should be performed without throwing errors.


# Test for various valid inputs for the update method
@pytest.mark.parametrize(
    "update_data",
    [
        ({"name": "Test1", "modified_by": "User1"}),
        ({"name": "Test2"}),
        (UpdateSchema(name="Test3")),
        (UpdateSchema(name="Test4", modified_by="User4")),
    ],
)
def test_update_various_inputs(db_session, update_data):
    dummy_db_obj = DummyModel(name="Old Name")
    db_session.add(dummy_db_obj)
    db_session.commit()

    updated_obj = crud_base.update(db_session, db_obj=dummy_db_obj, obj_in=update_data)

    assert (
        updated_obj is not None
    )  # The update should succeed with various valid inputs.
