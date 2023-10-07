
from main import *
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import Session, sessionmaker


import pytest
from app.settings import DATABASE_URL
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.models.book import Book


@pytest.fixture
def db_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def test_recreate_database(db_session: Session):
    # Execute before the recreate_database function is called
    with pytest.raises(OperationalError):
        db_session.query(Book).all()

    # Call the function
    recreate_database()

    # Execute after the recreate_database function is called to confirm it's working
    try:
        db_session.query(Book).all()
    except OperationalError as e:
        pytest.fail(f"OperationalError raised: {e}")
