from app.crud.crud_author import *
from fastapi.encoders import jsonable_encoder
from unittest.mock import MagicMock, Mock
from app.models.author import Author


from typing import Any, Dict, List, Union

import pytest
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase


@pytest.fixture
def db_session():
    return Mock(spec=Session)


@pytest.fixture
def crud_author():
    return CRUDAuthor()


def test_get_author_existing(db_session, crud_author):
    # Arrange
    test_author_id = 1
    test_author = Author(id=test_author_id, name="test author")
    db_session.query.return_value.filter.return_value.first.return_value = test_author

    # Act
    result = crud_author.get(db_session, test_author_id)

    # Assert
    db_session.query.assert_called_with(Author)
    db_session.query.return_value.filter.assert_called_with(Author.id == test_author_id)
    assert result == test_author


def test_get_author_nonexistent(db_session, crud_author):
    # Arrange
    test_author_id = 999
    db_session.query.return_value.filter.return_value.first.return_value = None

    # Act
    result = crud_author.get(db_session, test_author_id)

    # Assert
    db_session.query.assert_called_with(Author)
    db_session.query.return_value.filter.assert_called_with(Author.id == test_author_id)
    assert result is None


def test_get_author_multiple_results(db_session, crud_author):
    # Arrange
    test_author_id = 2
    multiple_authors = [
        Author(id=test_author_id, name="test author1"),
        Author(id=test_author_id, name="test author2"),
    ]
    db_session.query.return_value.filter.return_value.first.side_effect = (
        MultipleResultsFound
    )

    # Act and assert
    with pytest.raises(MultipleResultsFound):
        crud_author.get(db_session, test_author_id)

    db_session.query.assert_called_with(Author)
    db_session.query.return_value.filter.assert_called_with(Author.id == test_author_id)
