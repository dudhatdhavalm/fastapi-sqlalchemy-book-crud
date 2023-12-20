from app.models.book import Base
from sqlalchemy import create_engine
from app.settings import DATABASE_URL
from app.api.endpoints.book import *
from sqlalchemy.orm import Session, sessionmaker
import pytest


import pytest
from sqlalchemy.orm import Session

engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="function")
def db_session():
    """Provide a clean database session for each test."""
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    testing_session = SessionLocal()
    yield testing_session
    testing_session.close()
    Base.metadata.drop_all(engine)


def test_recreate_database(db_session):
    assert Base.metadata.tables != {}
    recreate_database()
    assert Base.metadata.tables != {}
