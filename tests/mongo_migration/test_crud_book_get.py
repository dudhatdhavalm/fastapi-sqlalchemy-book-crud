from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.crud.crud_book import *
import pymongo
from pymongo.collection import Collection
from bson.objectid import ObjectId
from unittest.mock import Mock
from pymongo import MongoClient

# Assuming that Mongo_URI and Mongo_DBName are the URI of your MongoDB and the name of your test database.
Mongo_URI = "your_mongodb_uri"
Mongo_DBName = "your_test_db_name"

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()  # Use the SQLAlchemy base class


# Assuming the following classes and functions are defined in the current scope:
# Book, MockCRUDBook

# Pymongo does not use the session pattern as SQLAlchemy does, instead it interacts directly with a collection object
# In this context, db_session would be a pymongo Collection object, not a SQLAlchemy Session.

@pytest.mark.parametrize("skip, limit", [(0, 10), (20, 20)])
def test_get_method_no_errors(db_collection: Collection, skip: int, limit: int):
    # Assuming MockCRUDBook's get method will work similar to pymongo's Collection.find() method
    crud_book = MockCRUDBook(Book)
    books_cursor = crud_book.get(db=db_collection, skip=skip, limit=limit)
    books = list(books_cursor)  # Convert cursor to list to work with the results
    assert (
        books is not None
    )  # Checking that the method call does not raise any exceptions


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)








class MockCRUDBook:

    def __init__(self, collection: Collection):
        self.collection = collection

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(collection.find().skip(skip).limit(limit))


Base.metadata.create_all(bind=engine)  # Create the tables in the in-memory SQLite DB


@pytest.fixture(scope="function")
def db_session():
    client = pymongo.MongoClient(Mongo_URI)
    db = client[Mongo_DBName]
    yield db
    # Clean up the database after the test
    db.drop_collection("books")
    client.close()


