from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base


import pytest
from app.crud.base import *
from typing import Any

import pytest

# Setup the test database
DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Fixture for the database session
@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def crud_base_class():
    return CRUDBase(Base)


def test_get_success(test_db: Session, crud_base_class: CRUDBase):
    result = crud_base_class.get(test_db, 1)
    assert result is not None


def test_get_failure(test_db: Session, crud_base_class: CRUDBase):
    result = crud_base_class.get(test_db, 0)
    assert result is None


def test_get_invalid_id_type(test_db: Session, crud_base_class: CRUDBase):
    with pytest.raises(Exception):
        crud_base_class.get(test_db, "invalid_id")


def test_get_nonexistent_id(test_db: Session, crud_base_class: CRUDBase):
    result = crud_base_class.get(test_db, 1000000)
    assert result is None


def test_get_negative_id(test_db: Session, crud_base_class: CRUDBase):
    with pytest.raises(Exception):
        crud_base_class.get(test_db, -1)
