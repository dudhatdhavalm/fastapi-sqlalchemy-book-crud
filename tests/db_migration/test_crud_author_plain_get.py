
from app.crud.crud_author_plain import *
from sqlalchemy.orm import Session
from app.crud.crud_author_plain import CRUDAuthor

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_db_session() -> MagicMock:
    return MagicMock(spec=Session)


@pytest.fixture
def mock_crud_author() -> CRUDAuthor:
    return CRUDAuthor()


def test_get_no_errors(
    mock_db_session: MagicMock, mock_crud_author: CRUDAuthor
) -> None:
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        []
    )
    result = mock_crud_author.get(db=mock_db_session)
    assert result is not None


def test_get_empty_list_when_db_is_empty(
    mock_db_session: MagicMock, mock_crud_author: CRUDAuthor
) -> None:
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        []
    )
    result = mock_crud_author.get(db=mock_db_session)
    assert isinstance(result, list)
    assert len(result) == 0
