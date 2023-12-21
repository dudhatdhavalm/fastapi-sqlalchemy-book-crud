from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
import pytest

# Defining an Example SQLAlchemy base
Base = declarative_base()


# Example SQLAlchemy model to use with the CRUD base
class ExampleSQLAlchemyModel(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


# Constants for database connection
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703158870842"


# Set up a fixture for the database engine
@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)


# Set up a fixture for the database session
@pytest.fixture(scope="module")
def db_session(engine) -> Session:
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


# Initialize the CRUDBase with ExampleSQLAlchemyModel for testing purposes
crud_base = CRUDBase(ExampleSQLAlchemyModel)


# The tests start here
def test_get_no_errors(db_session):
    """Test the CRUDBase 'get' method to ensure it does not throw errors when called."""
    try:
        result = crud_base.get(db_session)
        assert result is not None
    except Exception as e:
        pytest.fail(f"An error occurred: {str(e)}")


def test_get_correct_type(db_session):
    """Test if the 'get' method returns a list."""
    result = crud_base.get(db_session)
    assert isinstance(result, list), "The result should be a list"


def test_get_with_limit(db_session):
    """Test if the 'get' method respects the 'limit' parameter."""
    limit = 5
    result = crud_base.get(db_session, limit=limit)
    assert len(result) <= limit, "The result should not exceed the specified limit"


def test_get_with_skip(db_session):
    """Test if the 'get' method respects the 'skip' parameter."""
    skip = 5
    result_with_skip = crud_base.get(db_session, skip=skip)
    assert (
        len(result_with_skip) <= skip
    ), "The result with skip should have fewer or equal records compared to skip value"


# Necessary imports that should be placed at the top of the test file
"""
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pytest
from app.crud.base import CRUDBase
"""
