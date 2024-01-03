from sqlalchemy import Column, SmallInteger, create_engine
import pytest

from app.db.base_class import Base

from app.db.base_class import *


import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app.db.base_class import Base

# Set up in memory SQLite for testing purpose
test_engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(test_engine)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
)


# Using a simple subclass of Base to test __tablename__ generation
class DummyModel(Base):
    id = Column(SmallInteger, primary_key=True)


@pytest.fixture(scope="module")
def session():
    # Create a new database session for a test.
    connection = test_engine.connect()
    transaction = connection.begin()
    db_session = SessionLocal(bind=connection)
    yield db_session
    db_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def dummy_model_class():
    return DummyModel


def test_tablename_auto_generation(dummy_model_class):
    """Test that the __tablename__ attribute is automatically generated and not an error."""
    assert hasattr(
        dummy_model_class, "__tablename__"
    ), "Class does not have a __tablename__ attribute."
    assert dummy_model_class.__tablename__ is not None, "The __tablename__ is None."


def test_tablename_correctness(dummy_model_class):
    """Test that the __tablename__ attribute generates the correct table name based on class name."""
    expected_tablename = (
        "dummymodel".lower()
    )  # Assuming that __tablename__ is simply the lowercase of the class name
    assert (
        dummy_model_class.__tablename__ == expected_tablename
    ), f"The __tablename__ is incorrect. Expected {expected_tablename}, got {dummy_model_class.__tablename__}"
