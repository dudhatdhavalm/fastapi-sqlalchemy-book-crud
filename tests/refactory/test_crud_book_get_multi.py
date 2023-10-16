from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.book import Book
from typing import Generator
from app.crud.crud_book import *

import pytest


# Prepare DB session for testing
@pytest.fixture(scope="module")
def db() -> Generator:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/BooksDB"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()


def test_get_multi_no_error(db: Session) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db)
    assert books is not None


def test_get_multi_max_limit(db: Session) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, limit=100)
    assert len(books) <= 100


def test_get_multi_skip(db: Session) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, skip=1)
    if db.query(Book).count() > 1:
        assert len(books) == db.query(Book).count() - 1
    else:
        assert len(books) == 0


def test_get_multi_skip_and_limit(db: Session) -> None:
    crud = CRUDBook()
    books = crud.get_multi(db, skip=1, limit=1)
    if db.query(Book).count() > 1:
        assert len(books) == 1
    else:
        assert len(books) == 0
