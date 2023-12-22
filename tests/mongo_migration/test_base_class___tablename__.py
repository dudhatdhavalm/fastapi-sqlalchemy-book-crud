from app.db.base_class import *
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
import pytest




import pytest

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"

Base = declarative_base()


class Base(Base):
    __abstract__ = True  # Make sure SQLAlchemy knows this is an abstract class
    id = Column(Integer, primary_key=True)


class DummyModel(Base):
    __tablename__ = "dummy"


@pytest.fixture(scope="module")
def dummy_model_instance():
    return DummyModel()


# Assuming that 'DummyModel' is now a dictionary representing a MongoDB document.
# We'll also assume that there is a fixture 'dummy_model_instance' that properly sets up this dictionary for testing purposes.

def test_base_instantiation(dummy_model_instance):
    """
    Test that a document instance (representing the Base model in MongoDB) can be instantiated without errors.
    """
    assert dummy_model_instance is not None
    assert isinstance(dummy_model_instance, dict)  # MongoDB documents are represented as dictionaries in pymongo


def test_tablename(dummy_model_instance):
    """
    Test that the __tablename__ attribute is generated correctly.
    """
    assert dummy_model_instance.__tablename__ == "dummy"


def test_tablename_type(dummy_model_instance):
    """
    Test that the __tablename__ attribute is a string type.
    """
    assert isinstance(dummy_model_instance.__tablename__, str)
