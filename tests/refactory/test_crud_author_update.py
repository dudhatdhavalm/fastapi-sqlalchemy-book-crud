from sqlalchemy import create_engine
from app.crud.crud_author import *
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, Union
from app.models.author import Author

import pytest
from sqlalchemy.orm import clear_mappers, sessionmaker
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase


@pytest.fixture(scope="module")
def db():
    # Assuming connection string for your database
    engine = create_engine("postgresql://user:password@localhost/BooksDB")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@pytest.fixture(scope="module")
def crud_author(db):
    return CRUDAuthor(db)


def test_update(crud_author):
    # Arrange
    created_author = crud_author.create(
        obj_in={"name": "AuthorName", "book": "BookName"}
    )
    update_obj = {"name": "AuthorNameUpdate", "book": "BookNameUpdate"}

    # Act
    updated_author = crud_author.update(db_obj=created_author, obj_in=update_obj)

    # Assert
    assert updated_author.name == "AuthorNameUpdate"
    assert updated_author.book == "BookNameUpdate"
