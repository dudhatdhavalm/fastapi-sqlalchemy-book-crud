from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.models.author import Author


import pytest
from app.schemas.author import AuthorCreate
from datetime import date

import pytest
from app.crud.crud_author_plain import *


@pytest.fixture
def session() -> Session:
    return Session()


@pytest.fixture
def author_create() -> AuthorCreate:
    return AuthorCreate(name="Test Name", birth=date.today())


def test_create_method_no_throws(session, author_create):
    crud_author = CRUDAuthor()
    response = None
    try:
        response = crud_author.create(db=session, obj_in=author_create)
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected error: {e}")

    assert response is not None


def test_create_method_return_type(session, author_create):
    crud_author = CRUDAuthor()
    response = crud_author.create(db=session, obj_in=author_create)
    assert isinstance(response, Author)


def test_create_method_name_field(session, author_create):
    crud_author = CRUDAuthor()
    response = crud_author.create(db=session, obj_in=author_create)
    assert response.name == "Test Name"


def test_create_method_birth_field(session, author_create):
    crud_author = CRUDAuthor()
    response = crud_author.create(db=session, obj_in=author_create)
    assert response.birth == date.today()
