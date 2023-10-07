

from sqlalchemy import create_engine, inspect
from app.api.endpoints.book import *
from sqlalchemy import create_engine, inspect
from app.settings import DATABASE_URL
from app.models.book import Base
import pytest


@pytest.fixture(scope="module")
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="module")
def metadata():
    return Base.metadata


def test_recreate_database(engine, metadata):
    # Ensure that the BooksDB is empty before the test
    inspector = inspect(engine)
    assert not inspector.get_table_names()

    # Call target function
    recreate_database()

    # Check that the BooksDB has been created
    assert inspector.get_table_names()
