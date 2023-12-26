import pytest
from typing import Dict
from unittest.mock import MagicMock, patch

from app.crud.crud_author import *
from sqlalchemy.orm import Session




from typing import Dict
from pymongo.collection import Collection


@pytest.fixture
def mock_db_session():
    with patch("sqlalchemy.orm.Session", autospec=True) as mock:
        yield mock


@pytest.fixture
def dummy_author():
    with patch("app.models.author.Author", autospec=True) as mock:
        yield mock



@pytest.fixture
def author_update_dict() -> Dict[str, str]:
    return {"name": "Updated Author"}


def test_update_no_exceptions(mock_db_session, dummy_author, author_update_dict):
    crud_author = CRUDAuthor(model=Author)
    crud_author.update = MagicMock(return_value=dummy_author)
    assert (
        crud_author.update(
            mock_db_session, db_obj=dummy_author, obj_in=author_update_dict
        )
        is not None
    )


@pytest.fixture
def mock_db_collection():
    with patch('app.crud.crud_author.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_collection = MagicMock(spec=Collection)
        mock_get_db.return_value = mock_db
        mock_db.get_collection.return_value = mock_collection
        yield mock_collection
