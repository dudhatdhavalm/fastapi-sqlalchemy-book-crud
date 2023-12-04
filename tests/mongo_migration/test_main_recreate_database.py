from app.models.book import Base, Book
from sqlalchemy import create_engine
from app.settings import DATABASE_URL

from main import *
from sqlalchemy.orm import sessionmaker
import pytest
from pymongo import MongoClient

engine = create_engine(DATABASE_URL)


@pytest.fixture(scope="session")
def db_session():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test_database
    yield db
    client.close()


def test_recreate_database(db_session):
    try:
        db_session.drop_collection("books")
        recreate_database()
    except Exception as e:
        pytest.fail(f"recreate_database() raised {type(e)} exception")

    assert "books" in db_session.list_collection_names()
