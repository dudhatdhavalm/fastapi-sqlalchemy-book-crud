import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.crud.crud_author import *
from app.models.author import Author


import pytest


@pytest.fixture(scope="module")
def db_session():
    DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def new_author(db_session: Session):
    author = Author(id=1, name="John Doe", book="Test Book")
    db_session.add(author)
    db_session.commit()
    return author


def test_get_exists(db_session: Session, new_author: Author):
    crud_author = CRUDAuthor()
    author = crud_author.get(db_session, new_author.id)
    assert author is not None
    assert author.id == new_author.id


def test_get_not_exists(db_session: Session):
    crud_author = CRUDAuthor()
    author = crud_author.get(db_session, 9999)
    assert author is None
