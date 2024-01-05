import pytest
from app.crud.base import CRUDBase

from app.crud.base import *

from app.crud.base import CRUDBase
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, sessionmaker


import pytest
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def crud_base_instance():
    return CRUDBase(DummyModel)


def test_get_by_id_no_errors(crud_base_instance, db_session):
    # Test the get_by_id method to ensure it does not produce any errors.
    # Populating the database with a dummy entry for the test.
    dummy_object = DummyModel(id=1)
    db_session.add(dummy_object)
    db_session.commit()

    # Fetching the same entry using the get_by_id method.
    result = crud_base_instance.get_by_id(db_session, 1)
    assert (
        result is not None
    ), "get_by_id should return a non-None result when a matching ID is found."


@pytest.mark.parametrize("test_id", [2, "not-an-id", None])
def test_get_by_id_invalid_id(crud_base_instance, db_session, test_id):
    # Should return None when no records found with the given ID.
    result = crud_base_instance.get_by_id(db_session, test_id)
    assert (
        result is None
    ), f"get_by_id should return None for non-existent or invalid ID: {test_id}"
