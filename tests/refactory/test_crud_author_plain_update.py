from sqlalchemy import create_engine, sessionmaker
from unittest.mock import Mock
from app.crud.crud_author_plain import *

from app.models.author import Author
from typing import Union
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def sample_author():
    author = Author(id=1, name="Author", dob=date(1990, 5, 5))
    return author


@pytest.fixture
def database():
    engine = create_engine("postgresql://username:password@localhost:5432/BooksDB")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_update_object(sample_author, database):
    crud_author = CRUDAuthor()

    sample_author.name = "Updated author"
    updated_author = crud_author.update(
        db=database, db_obj=sample_author, obj_in=sample_author
    )

    assert updated_author.name == "Updated author"


def test_update_dict(sample_author, database):
    crud_author = CRUDAuthor()

    updated_author = crud_author.update(
        db=database, db_obj=sample_author, obj_in={"name": "Updated author"}
    )
