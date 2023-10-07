from datetime import date
from app.crud.crud_author_plain import *
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate


@pytest.fixture
def setup_db():
    session = Session(bind=engine)
    Base.metadata.create_all(engine)
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def author_data():
    return AuthorCreate(name="John Doe", birth_date=date(1960, 1, 1))


def test_create_author(setup_db, author_data):
    author_crud = CRUDAuthor()

    author = author_crud.create(db=setup_db, obj_in=author_data)

    assert author.id is not None
    assert author.name == "John Doe"
    assert author.birth_date == date(1960, 1, 1)

    # Test with invalid birth_date
    invalid_author_data = AuthorCreate(
        name="Invalid Author", birth_date=date(1820, 1, 1)
    )

    with pytest.raises(
        ValueError, match="Author's birth_date should be greater than 1900"
    ):
        author_crud.create(db=setup_db, obj_in=invalid_author_data)
