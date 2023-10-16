import pytest
from sqlalchemy import Column, Integer, Sequence, String, create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.models.author import Author


import pytest
from sqlalchemy.ext.declarative import declarative_base
from app.crud.crud_author_plain import *
from pymongo import MongoClient

Base = declarative_base()


class TestAuthor(Base):
    __tablename__ = "authors"

    id = Column(Integer, Sequence("author_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)

    def __init__(self, name):
        self.name = name


@pytest.fixture(scope="module")
def db() -> MongoClient:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_db
    return db


def test_get_all(client: MongoClient):
    crud_author = CRUDAuthor()

    # Mock data
    test_authors = [{"name": f"Author {i}"} for i in range(10)]
    authors_collection = client.db["authors"]
    result = authors_collection.insert_many(test_authors)

    authors = crud_author.get_all(client)
    assert authors is not None
    assert authors.count() >= 1

    # Cleanup
    for author in test_authors:
        query = {"_id": author["_id"]}
        authors_collection.delete_one(query)
