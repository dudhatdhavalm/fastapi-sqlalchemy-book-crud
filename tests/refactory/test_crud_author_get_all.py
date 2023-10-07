from app.crud.crud_author import *
from typing import List
from app.models.author import Author

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def sample_author(db: Session):
    # Create a sample author instance
    author = Author(name="Sample Author")
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.mark.parametrize(
    "skip, limit, expected_result",
    [
        (0, 1, ["Sample Author"]),
        (1, 1, []),
        (0, 0, []),
    ],
)
def test_get_all(
    db: Session,
    sample_author: Author,
    skip: int,
    limit: int,
    expected_result: List[str],
):
    crud_author = CRUDAuthor()
    authors = crud_author.get_all(db, skip=skip, limit=limit)
    assert [author.name for author in authors] == expected_result


@pytest.mark.parametrize(
    "skip, limit",
    [
        (-1, 1),
        (0, -1),
    ],
)
def test_get_all_invalid_skip_limit(db: Session, skip: int, limit: int):
    crud_author = CRUDAuthor()
    with pytest.raises(ValueError):
        crud_author.get_all(db, skip=skip, limit=limit)
