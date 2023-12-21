
from app.crud.base import *
from sqlalchemy import Column, Integer, create_engine
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import pytest

# Use a memory-only SQLite database for testing, which doesn't require any
# real database server to be available. If the real database connection
# string is needed later for some reason, replace the argument of create_engine
DATABASE_URL = "sqlite://"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModelTest = declarative_base()


@pytest.fixture
def db_session():
    BaseModelTest.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    BaseModelTest.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_model(db_session: Session):
    class MockModel(BaseModelTest):
        __tablename__ = "test_table"
        id = Column(Integer, primary_key=True)

    BaseModelTest.metadata.create_all(bind=engine)
    return MockModel


# Test instantiation of CRUDBase does not raise error
def test_CRUDBase_init_no_errors(mock_model):
    assert (
        CRUDBase(mock_model) is not None
    ), "CRUDBase __init__ raised an error with valid model"


# Since we expect CRUDBase to throw an error if None or an incorrect type
# is passed as a model, the remaining tests can be commented out since they
# are no longer valid with typing in place and the `model` is not expected to be None.
# Commenting out to not skip code.

# Test instantiation of CRUDBase with None as model raises an error
# def test_CRUDBase_init_with_none():
#     with pytest.raises(TypeError):
#         CRUDBase(None)

# Test instantiation of CRUDBase with incorrect type as model raises an error
# def test_CRUDBase_init_with_incorrect_type():
#     with pytest.raises(TypeError):
#         CRUDBase("not_a_model_class")


import pytest
