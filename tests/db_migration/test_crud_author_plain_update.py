
from app.crud.crud_author_plain import *
import pytest


# necessary fixtures and sample data for the test
@pytest.fixture
def sample_author_db_obj():
    return Author(id=1, name="Authorname")


@pytest.fixture
def sample_author_obj_in():
    return AuthorCreate(name="NewAuthorname")


@pytest.fixture
def sample_dict_obj_in():
    return {"name": "NewAuthorname"}


# unittests
def test_update_does_not_throw_errors_with_sample_data(
    sample_author_db_obj, sample_author_obj_in
):
    with Session() as db:
        crud_author = CRUDAuthor()
        updated_author = crud_author.update(
            db=db, db_obj=sample_author_db_obj, obj_in=sample_author_obj_in
        )
        assert updated_author is not None, "Updated author should not be None"


def test_update_changes_author_data_with_author_object(
    sample_author_db_obj, sample_author_obj_in
):
    with Session() as db:
        old_name = sample_author_db_obj.name
        crud_author = CRUDAuthor()
        updated_author = crud_author.update(
            db=db, db_obj=sample_author_db_obj, obj_in=sample_author_obj_in
        )
        assert updated_author.name != old_name, "Author name should be updated"


def test_update_changes_author_data_with_dict(sample_author_db_obj, sample_dict_obj_in):
    with Session() as db:
        old_name = sample_author_db_obj.name
        crud_author = CRUDAuthor()
        updated_author = crud_author.update(
            db=db, db_obj=sample_author_db_obj, obj_in=sample_dict_obj_in
        )
        assert updated_author.name != old_name, "Author name should be updated"


def test_update_does_not_change_data_when_empty_dict(sample_author_db_obj):
    with Session() as db:
        old_name = sample_author_db_obj.name
        crud_author = CRUDAuthor()
        updated_author = crud_author.update(
            db=db, db_obj=sample_author_db_obj, obj_in={}
        )
        assert (
            updated_author.name == old_name
        ), "Author name should not be updated when empty dict is given"


def test_update_returns_same_author_when_same_data_given(sample_author_db_obj):
    with Session() as db:
        crud_author = CRUDAuthor()
        updated_author = crud_author.update(
            db=db, db_obj=sample_author_db_obj, obj_in=sample_author_db_obj
        )
        assert (
            updated_author.id == sample_author_db_obj.id
        ), "Author ID should remain same when the same author is given"
        assert (
            updated_author.name == sample_author_db_obj.name
        ), "Author name should remain same when the same author is given"
