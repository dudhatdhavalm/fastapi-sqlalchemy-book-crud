from datetime import date
from app.crud.crud_author_plain import *


import pytest
from app.models.author import Author

import pytest
from sqlalchemy.orm import Session


def setup_module():
    # Assume we have a function `init_database` which is used to initialize the database
    init_database()


@pytest.fixture
def db():
    # Assuming that we have a function `get_db_session` which returns db session
    session = get_db_session()
    yield session
    session.close()


def test_get_author_exists(db: Session):
    # Considering the author with id `1` is already present in the database
    crud_author = CRUDAuthor()
    author = crud_author.get(db, 1)
    assert author is not None
    assert author.id == 1
    assert isinstance(author, Author)


def test_get_author_doesnot_exist(db: Session):
    # Let's query for an author with an id `99999` which does not exist in our database
    crud_author = CRUDAuthor()
    author = crud_author.get(db, 99999)
    assert author is None


def test_get_author_with_invalid_id(db: Session):
    # Let's query for an author with an id `-1` (invalid id)
    crud_author = CRUDAuthor()
    with pytest.raises(ValueError):
        crud_author.get(db, -1)
