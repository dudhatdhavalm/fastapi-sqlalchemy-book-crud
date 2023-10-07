from sqlalchemy.engine import Engine


import pytest
from app.models.author import Author
from sqlalchemy import create_engine, inspect
from app.api.endpoints.author import *
from sqlalchemy import inspect
import pytest


@pytest.fixture
def engine():
    return create_engine(DATABASE_URL)


@pytest.fixture
def author_table(engine: Engine):
    return engine.table_names().include("author")


def test_recreate_database(engine, author_table):
    recreate_database()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert (
        "author" in tables
    ), f"'author' table not found in database after running recreate_database()"

    fields = inspector.get_columns("author")
    assert isinstance(fields, list), "'author' table is not properly set up"

    expected_field_names = set(field.name for field in Author.__table__.columns)
    actual_field_names = set(field["name"] for field in fields)

    assert (
        expected_field_names == actual_field_names
    ), "'author' table does not match expected schema"
