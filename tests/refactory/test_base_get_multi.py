from app.db.base_class import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from unittest.mock import MagicMock, patch
from app.crud.base import *


from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(scope="module")
def test_db():
    # Creating a new database on the fly
    # don't worry about cleaning it in the future
    engine = create_engine("postgresql://localhost/BooksDBTest")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@pytest.fixture
def crud_base_mock():
    with patch("app.CRUD_base.CRUD_base", autospec=True) as mock:
        yield mock


def test_get_multi_skip_limit(test_db: Session, crud_base_mock):
    # creating a CRUD object with the mock model
    crud_base = crud_base_mock(model=MagicMock())
    crud_base.get_multi(test_db, skip=0, limit=100)

    # Check if the methods offset and limit were called with appropriate values
    crud_base_mock.query().offset.assert_called_with(0)
    crud_base_mock.query().limit.assert_called_with(100)


def test_get_multi_no_skip_limit(test_db: Session, crud_base_mock):
    # creating a CRUD object with the mock model
    crud_base = crud_base_mock(model=MagicMock())
    crud_base.get_multi(test_db)

    # Check if the methods offset and limit were called with default values
    crud_base_mock.query().offset.assert_called_with(0)
    crud_base_mock.query().limit.assert_called_with(100)
