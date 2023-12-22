# Import required standard library and pytest fixtures
import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base


import pytest

# Database connection string
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"

# Set up the test session and engine using the provided database string
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()


# Provide a SQLAlchemy model for testing purposes
class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


# Pytest fixture to create a new database session for testing
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def crud_base(db_session: Session):
    # CRUDBase is taken from the current file's scope
    return CRUDBase(DummyModel)


# Test to verify that calling the function doesn't throw errors
def test_get_no_errors(crud_base, db_session):
    assert crud_base.get(db_session) is not None


# Test to verify 'limit' parameter functionality
def test_get_limit_parameter(crud_base, db_session):
    assert len(crud_base.get(db_session, limit=10)) <= 10


# Test to verify 'skip' parameter functionality
def test_get_skip_parameter(crud_base, db_session):
    all_data = crud_base.get(db_session, limit=10)
    skipped_data = crud_base.get(db_session, skip=5, limit=5)
    assert all_data[5:] == skipped_data
