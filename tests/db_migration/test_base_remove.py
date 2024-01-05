import pytest

from app.crud.base import *
from sqlalchemy.orm import sessionmaker


from sqlalchemy import Column, Integer, create_engine
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704487699809"

# Define a base model for creating database tables
Base = declarative_base()


# Define a sample model for testing
class SampleModel(Base):
    __tablename__ = "sample_model"
    id = Column(Integer, primary_key=True, index=True)


# Setup test database and tables
@pytest.fixture(scope="module")
def test_db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_db_session(test_db_engine):
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = session_local()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def crud_base(test_db_session):
    # Assuming CRUDBase exists in app.crud.base and is imported as such
    return CRUDBase(model=SampleModel)


def test_remove_does_not_raise_error(crud_base, test_db_session):
    # Ensure the database is clean before the test
    test_db_session.query(SampleModel).delete()
    test_db_session.commit()

    # Create an object so we can remove it
    sample = SampleModel()
    test_db_session.add(sample)
    test_db_session.commit()
    assert crud_base.remove(db=test_db_session, id=sample.id) is not None


def test_remove_returns_correct_type(crud_base, test_db_session):
    # Ensure the database is clean before the test
    test_db_session.query(SampleModel).delete()
    test_db_session.commit()

    # Create an object to remove and test return value
    sample = SampleModel()
    test_db_session.add(sample)
    test_db_session.commit()
    removed_obj = crud_base.remove(db=test_db_session, id=sample.id)
    assert isinstance(removed_obj, SampleModel)
