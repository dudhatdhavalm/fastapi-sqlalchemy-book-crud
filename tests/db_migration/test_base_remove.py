
from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, create_engine

import pytest
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock

# We define a SQL Alchemy Base model for mocking.
Base = declarative_base()


# Define a Dummy SQLAlchemy model for testing
class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)


@pytest.fixture
def db_session():
    """Create a mock session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    db_mock = Mock(wraps=session)

    # Making sure that dummy_db_session closes the session after use.
    yield db_mock
    session.close()


@pytest.fixture
def crud_base_instance():
    # Create an instance of CRUDBase with the DummyModel
    return CRUDBase(DummyModel)


# Tests
def test_remove_does_not_raise_error(crud_base_instance, db_session):
    # Assure the `remove` method does not throw errors when executed and that the returned value is not None
    dummy_instance = DummyModel()
    db_session.add(dummy_instance)
    db_session.commit()
    assert crud_base_instance.remove(db=db_session, id=1) is not None


# ... The rest of the tests would be similar, updating the session fixture as we start with db_session().


from sqlalchemy import Column, Integer, create_engine
