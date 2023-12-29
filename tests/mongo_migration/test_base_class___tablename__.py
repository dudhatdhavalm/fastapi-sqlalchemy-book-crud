from sqlalchemy.orm import declarative_base

from app.db.base_class import BaseDefault


import pytest
from sqlalchemy import create_engine
from sqlalchemy import Column, SmallInteger
import pytest

from app.db.base_class import *
from sqlalchemy import Column, SmallInteger, create_engine

DATABASE_URI = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
engine = create_engine(DATABASE_URI)

# Reflect the declarative base from the existing Base class
Base = declarative_base(cls=BaseDefault)

# To use in tests, we need to ensure the engine is using the correct database URI
Base.metadata.bind = engine


@pytest.fixture(scope="module")
def dummy_model():
    """Fixture for creating a test model that inherits from the Base class."""

    class DummyModel(Base):
        id = Column(SmallInteger, primary_key=True)

    # Ensure that the table name is extracted from the class name as expected
    assert (
        DummyModel.__tablename__ == "dummymodel"
    ), "The __tablename__ should be autogenerated correctly from the class name"

    # Create the DummyModel table in the database for testing purposes.
    Base.metadata.create_all(bind=engine)
    yield DummyModel

    # Clean up the created table after testing
    Base.metadata.drop_all(bind=engine)


def test_tablename_autogeneration(dummy_model):
    """
    Test that the __tablename__ is automatically generated using the name of the class.
    """
    assert dummy_model.__tablename__ is not None, "The __tablename__ should not be None"
    assert (
        dummy_model.__tablename__ == "dummymodel"
    ), "The __tablename__ should be 'dummymodel'"


# Note: additional edge case tests can be added below.


import pytest