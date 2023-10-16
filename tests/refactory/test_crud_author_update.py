from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.crud.crud_author import *
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.author import CRUDAuthor

import pytest
from typing import Any, Dict, Union

DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db: Session = SessionLocal()


@pytest.fixture(scope="module")
def test_author():
    return Author(
        id=1,
        name="Test Author",
    )


@pytest.fixture(scope="module")
def update_author():
    return {"name": "Updated Test Author"}


def test_update(test_author, update_author):
    crud_author = CRUDAuthor()
    updated_author = crud_author.update(db=db, db_obj=test_author, obj_in=update_author)
    assert updated_author is not None
    assert updated_author.name == "Updated Test Author"
