import pytest
from app.schemas.author import AuthorCreate

from app.crud.crud_author_plain import *


from datetime import date
from app.models.author import Author
from unittest import mock
from sqlalchemy.orm import Session

from app.crud.crud_author_plain import CRUDAuthor

import pytest


@pytest.fixture
def test_session():
    engine = create_engine("postgresql://postgres:root@host.docker.internal:5432/")
    Session.configure(bind=engine)
    return Session()

sample_author_create = AuthorCreate(name="Test Author", birthdate=date(1990, 1, 1))


@pytest.fixture
def crud_author():
    return CRUDAuthor()


# edge case: test if the function doesn't throw errors when it's executed
def test_create_no_error(crud_author):
    with mock.patch.object(Session, "add") as mock_add, mock.patch.object(
        Session, "commit"
    ) as mock_commit, mock.patch.object(Session, "refresh") as mock_refresh:
        result = crud_author.create(db=Session(), obj_in=sample_author_create)

        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_refresh.assert_called_once()

        assert result is not None


# edge case: test if the returned object is an instance of "Author"
def test_create_return_class(crud_author):
    with mock.patch.object(Session, "add") as mock_add, mock.patch.object(
        Session, "commit"
    ) as mock_commit, mock.patch.object(Session, "refresh") as mock_refresh:
        result = crud_author.create(db=Session(), obj_in=sample_author_create)

        assert isinstance(result, Author)
