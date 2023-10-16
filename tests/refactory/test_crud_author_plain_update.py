import pytest
from app.crud.crud_author_plain import *
from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate


from datetime import date

import pytest
from app.crud.base import CRUDBase


def test_update_no_error(db_session):
    crud_author = CRUDAuthor()
    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": date.today(),
    }
    new_author = crud_author.create(db_session, obj_in=author_data)
    update_data = {"name": "updated_name"}
    updated_author = crud_author.update(
        db_session, db_obj=new_author, obj_in=update_data
    )
    assert updated_author is not None
    assert updated_author.name == "updated_name"


def test_update_with_model_instance(db_session):
    crud_author = CRUDAuthor()
    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": date.today(),
    }
    new_author = crud_author.create(db_session, obj_in=author_data)
    update_model = Author(**{"name": "updated_name"})
    updated_author = crud_author.update(
        db_session, db_obj=new_author, obj_in=update_model
    )
    assert updated_author is not None
    assert updated_author.name == "updated_name"


def test_update_keep_old_value_if_not_in_dict(db_session):
    crud_author = CRUDAuthor()
    author_data = {
        "name": "test_name",
        "email": "test@example.com",
        "birth_date": date.today(),
    }
    new_author = crud_author.create(db_session, obj_in=author_data)
    update_data = {"email": "updated@example.com"}
    updated_author = crud_author.update(
        db_session, db_obj=new_author, obj_in=update_data
    )
    assert updated_author is not None
    assert updated_author.email == "updated@example.com"
    assert updated_author.name == "test_name"
