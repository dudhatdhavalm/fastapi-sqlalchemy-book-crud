from app.db.base_class import Base


from sqlalchemy import Column, Integer, create_engine
from app.crud.base import CRUDBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from app.crud.base import *
from sqlalchemy.orm import Session, sessionmaker


# Use the Base class from app.db.base_class to make a fake model
class FakeModel(Base):
    __tablename__ = "fake_model"
    id = Column(Integer, primary_key=True)


# Generate the database URL from the variables or just hardcode as below
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"


# Fixtures for setting up the database connection and session
@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="module")
def SessionLocal(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session(SessionLocal):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Tests for CRUDBase __init__ method
def test_crudbase_init_no_errors():
    """
    Test that the __init__ method of CRUDBase can be called with a model class
    and does not raise any exceptions.
    """
    try:
        crud_base_instance = CRUDBase(FakeModel)
        assert crud_base_instance is not None
        assert issubclass(crud_base_instance.model, Base)
    except Exception as e:
        pytest.fail(f"CRUDBase __init__ raised an exception: {e}")
