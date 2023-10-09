from app.crud.crud_author import *
from typing import List
from app.models.author import Author

import pytest
from sqlalchemy.orm import Session
from pymongo import MongoClient


@pytest.fixture
def sample_author():
    # Instantiate client
    client = MongoClient('localhost', 27017)

    # Choose a specific database (replace 'mydb' with your database)
    db = client['mydb']

    # Create a sample author instance
    author = {"name": "Sample Author"}

    # Insert the author into the collection of authors (replace 'authors' with your collection)
    db.authors.insert_one(author)

    # Close the client connection
    client.close()

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
    db: MongoClient,
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
def test_get_all_invalid_skip_limit(db: MongoClient, skip: int, limit: int):
    crud_author = CRUDAuthor()
    with pytest.raises(ValueError):
        crud_author.get_all(db, skip=skip, limit=limit)
