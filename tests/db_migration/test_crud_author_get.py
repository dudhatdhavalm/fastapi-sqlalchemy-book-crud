from sqlalchemy.orm import sessionmaker

import pytest
from sqlalchemy import create_engine

from app.crud.crud_author import CRUDAuthor
from sqlalchemy.exc import SQLAlchemyError


from unittest.mock import MagicMock
from unittest.mock import MagicMock
from app.models.author import Author

from app.crud.crud_author import *


# Mock classes
class _BaseMock:
    query = MagicMock()


class _QueryMock:
    def offset(self, num):
        return self

    def limit(self, num):
        return self

    def all(self):
        return []


# The DATABASE_URI is provided according to the user's instructions
DATABASE_URI = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"


@pytest.fixture(scope="module")
def db_engine():
    return create_engine(DATABASE_URI)


@pytest.fixture(scope="module")
def db_session_factory(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    return SessionLocal


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    session = db_session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def crud_author():
    return CRUDAuthor(Author)


def test_get_method_executes_without_error(db_session, crud_author):
    db_session.query = MagicMock(return_value=_QueryMock())
    try:
        authors = crud_author.get(db_session)
    except SQLAlchemyError as e:
        pytest.fail(f"Unexpected SQLAlchemyError occurred: {e}")
    assert (
        authors is not None
    ), "The `get` method should return a result, even if it's an empty list"
