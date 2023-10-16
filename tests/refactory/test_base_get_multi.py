import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from app.crud import CRUDBase
from app.crud.base import *
from app.models import Book


from typing import Generator
from sqlalchemy.orm import sessionmaker

from app.crud import CRUDBase


# Define a fixture for the database session
@pytest.fixture(scope="module")
def db() -> Generator:
    engine = create_engine("postgresql://postgres:root@localhost/BooksDB")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()
    yield session
    session.close()


# Test to check if function doesn't throw any errors when executed
# and it returns data (the function should return a list)
def test_get_multi_no_errors(db: Session):
    crud = CRUDBase(Book)
    result = crud.get_multi(db)
    assert result is not None


# Test to check for working of skip and limit parameters
def test_get_multi_skip_limit(db: Session):
    crud = CRUDBase(Book)
    all_books = crud.get_multi(db)
    skipped_books = crud.get_multi(db, skip=1)
    limited_books = crud.get_multi(db, limit=1)

    # If books are present in db
    if all_books:
        assert len(skipped_books) == len(all_books) - 1
        assert len(limited_books) == 1


# Test to check if providing very high skip doesn't cause errors
def test_get_multi_high_skip(db: Session):
    crud = CRUDBase(Book)
    result = crud.get_multi(db, skip=9999)
    assert result is not None


# Test to check if providing negative limit and skip doesn't cause errors
def test_get_multi_negative_skip_limit(db: Session):
    crud = CRUDBase(Book)
    result = crud.get_multi(db, skip=-9999, limit=-9999)
    assert result is not None
