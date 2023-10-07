from datetime import date
from app.crud.crud_author_plain import *

from app.models.author import Author
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def db_session():
    db = Session()
    yield db
    db.close()


@pytest.fixture
def sample_author():
    return Author(id=1, name="John Doe", birth_date=date(2000, 1, 1))


def test_get_all_empty(db_session):
    crud_author = CRUDAuthor()
    result = crud_author.get_all(db_session)
    assert isinstance(result, list)
    assert len(result) == 0


def test_get_all_with_data(db_session, sample_author):
    db_session.add(sample_author)
    db_session.commit()
    crud_author = CRUDAuthor()
    result = crud_author.get_all(db_session)
    assert isinstance(result, list)
    assert len(result) == 1
    author = result[0]
    assert author.id == 1
    assert author.name == "John Doe"
    assert author.birth_date == date(2000, 1, 1)


def test_get_all_with_skip_limit(db_session):
    for i in range(5):
        author = Author(id=i, name=f"Author {i}", birth_date=date(2000, 1, 1))
        db_session.add(author)
    db_session.commit()

    crud_author = CRUDAuthor()

    result = crud_author.get_all(db_session, skip=1, limit=2)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

    result = crud_author.get_all(db_session, skip=3, limit=1)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 3
