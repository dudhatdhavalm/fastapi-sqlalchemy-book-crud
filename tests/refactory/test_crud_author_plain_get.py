from sqlalchemy.orm import Session
from typing import Any, Dict, List, Union
from fastapi.encoders import jsonable_encoder


from app.crud import CRUDAuthor
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from sqlalchemy import create_engine, engine, sessionmaker
from datetime import date

import pytest
from app.crud.crud_author_plain import *

# Fixtures


@pytest.fixture
def db_session():
    # Create session and add base test case
    engine = create_engine(f"postgresql://postgres:root@localhost:5432/BooksDB-test")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    base_author = AuthorCreate(name="Author name", date_of_birth=date(1990, 1, 1))
    base_author_db = db_model.Author(**base_author.dict())
    db.session.add(base_author_db)
    db.session.commit()
    yield session
    session.close()
    engine.dispose()


# Test Cases


def test_get(db_session):
    author_crud = CRUDAuthor()
    fetched_author = author_crud.get(db_session, 1)
    assert fetched_author is not None, f"function returned None, expected Author object"
    assert isinstance(
        fetched_author, Author
    ), f"function returned {type(fetched_author).__name__}, expected Author"


def test_get_invalid_id(db_session):
    author_crud = CRUDAuthor()
    fetched_author = author_crud.get(db_session, 100)
    assert (
        fetched_author is None
    ), f"function returned an author object for a non-existing id, expected None"
