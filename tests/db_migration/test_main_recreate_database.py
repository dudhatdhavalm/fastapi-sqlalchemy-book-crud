from app.models.book import Base, Book
from sqlalchemy import create_engine
from app.settings import DATABASE_URL

from main import *
from sqlalchemy.orm import sessionmaker
import pytest

engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session")
def db_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_recreate_database(db_session):
    # this is the most important test, we just want to check if the function doesn't throw any errors
    try:
        Base.metadata.drop_all(engine)
        recreate_database()
    except Exception as e:
        pytest.fail(f"recreate_database() raised {type(e)} exception")

    # also might be a good check if table exists in the database after `recreate_database()`
    assert "books" in db_session.bind.table_names()
