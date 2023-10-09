from main import *
from sqlalchemy import create_engine
import pytest
from sqlalchemy.orm import Session, sessionmaker


import pytest
from app.settings import DATABASE_URL
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.models.book import Book
from pymongo import MongoClient
from pymongo import MongoClient, errors



@pytest.fixture
def db_session():
    client = MongoClient(DATABASE_URL)
    db = client.get_default_database()
    return db


def test_recreate_database(client: MongoClient):
    # Execute before the recreate_database function is called
    with pytest.raises(errors.ServerSelectionTimeoutError):
        client.db.books.find()

    # Call the function
    recreate_database()

    # Execute after the recreate_database function is called to confirm it's working
    try:
        client.db.books.find()
    except errors.ServerSelectionTimeoutError as e:
        pytest.fail(f"ServerSelectionTimeoutError raised: {e}")
