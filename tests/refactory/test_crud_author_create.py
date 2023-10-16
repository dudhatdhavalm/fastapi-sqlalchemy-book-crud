import pytest
from sqlalchemy.orm import Session
from app.crud.crud_author import *
from app.models.author import Author


import pytest
from app.schemas.author import AuthorCreate
from app.crud.crud_author import CRUDAuthor


def test_create():
    # Testing for normal input values
    name = "Test Author"
    CRUDAuthor_obj = CRUDAuthor()
    assert (
        CRUDAuthor_obj.create(db=Session(), obj_in=AuthorCreate(name=name)) is not None
    )

    # Testing for empty input
    name = ""
    CRUDAuthor_obj = CRUDAuthor()
    assert (
        CRUDAuthor_obj.create(db=Session(), obj_in=AuthorCreate(name=name)) is not None
    )

    # Test to handle invalid type inputs that create SQLAlchmey errors
    with pytest.raises(Exception):
        name = 1234  # given name as integer, should raise an Exception
        CRUDAuthor_obj = CRUDAuthor()
        CRUDAuthor_obj.create(db=Session(), obj_in=AuthorCreate(name=name))


def setup_function(function):
    print(f"setting up {function}")
    # Initial setup for the function. Create a new session, or maybe a test environment?


def teardown_function(function):
    print(f"tearing down {function}")
    # Clean the test environment, delete the session etc.
