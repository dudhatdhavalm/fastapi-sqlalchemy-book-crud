from app.crud.crud_author import *
from app.crud.crud_author import CRUDAuthor
from unittest.mock import Mock, patch
from app.models.author import Author

import pytest
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate


@patch(
    "app.crud.crud_author.jsonable_encoder", return_value={"id": 1, "name": "John Doe"}
)
@patch("sqlalchemy.orm.Session.commit")
@patch("sqlalchemy.orm.Session.add")
@pytest.mark.parametrize(
    "author_input",
    [
        ({"id": 1, "name": "John Doe"}),
        ({"id": 2, "name": "Jane Doe"}),
    ],
)
def test_create(mock_add, mock_commit, mock_jsonable_encoder, author_input):
    session = Mock(spec=Session)
    author_crud = CRUDAuthor()
    author_schema = AuthorCreate(**author_input)

    result = author_crud.create(session, obj_in=author_schema)

    mock_jsonable_encoder.assert_called_once_with(author_schema)
    mock_add.assert_called_once()
    mock_commit.assert_called_once()
    assert isinstance(result, Author)
    assert result.id == author_input["id"]
    assert result.name == author_input["name"]


@pytest.fixture
def setup_faulty_data():
    return AuthorCreate(id=None, name="John Doe")


def test_create_with_faulty_data(setup_faulty_data):
    session = Mock(spec=Session)
    author_crud = CRUDAuthor()

    with pytest.raises(Exception):
        author_crud.create(session, obj_in=setup_faulty_data)
