from sqlalchemy.orm import Session, sessionmaker
from app.models.book import Book
from sqlalchemy import create_engine
import pytest

from app.crud.crud_book_plain import *
from app.schemas.book import BookCreate
from app.db.base_class import Base





from app.crud.crud_book_plain import CRUDBook
from pymongo import MongoClient
from pymongo.collection import Collection

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# The BookCreate schema needs to be adapted to Python dictionary, since PyMongo uses dictionaries
def book_create_payload():
    return {"title": "Test Book", "pages": 123, "author_id": 1}

@pytest.fixture(scope="module")
def book_create_payload():
    return book_create_payload()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    client = get_mongo_client() 
    yield client.testdb  # This should yield the database instance to be used
    client.close()

@pytest.fixture(scope="module")
def books_collection(db):
    return db.books  # 'books' is assumed to be the name of the collection


@pytest.fixture(scope="module")
def db_session():
    client = MongoClient(MONGODB_DATABASE_URL)
    db = client[MONGODB_DATABASE_NAME]
    book_collection = db['book']
    # The collection is being emptied to ensure a clean state before the tests run
    book_collection.delete_many({})

    yield book_collection

    # Clean up: drop the collection after the tests run
    book_collection.drop()
    client.close()


def test_create_book_without_errors(
    db_session: Session, book_create_payload: BookCreate
):
    crud_book = CRUDBook()
    result = crud_book.create(db=db_session, obj_in=book_create_payload)
    assert (
        result is not None
    ), "The create method should return a Book instance, not None"
