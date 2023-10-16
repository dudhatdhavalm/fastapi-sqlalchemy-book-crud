import pytest
from app.models.author import Base


import pytest
from app.api.endpoints.author import *
from sqlalchemy import create_engine, text
from sqlalchemy import text


@pytest.fixture(scope="module")
def engine():
    DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"
    return create_engine(DATABASE_URL)


@pytest.fixture(scope="module")
def connection(engine):
    return engine.connect()


@pytest.fixture(scope="module")
def transaction(connection):
    trans = connection.begin()
    yield
    trans.rollback()


@pytest.mark.usefixtures("transaction")
def test_recreate_database(engine, connection):
    recreate_database()

    # Check if tables are created
    result = connection.execute(
        text("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
    )
    tables = [row["table_name"] for row in result]
    assert "author" in tables
    assert "book" in tables


@pytest.mark.usefixtures("transaction")
def test_recreate_database_no_errors():
    # This test is just to make sure the command doesn't throw any exceptions,
    # not to check if the tables are correctly created.
    assert recreate_database() is None
