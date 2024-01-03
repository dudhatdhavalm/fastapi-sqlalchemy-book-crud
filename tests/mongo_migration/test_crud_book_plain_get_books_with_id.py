from app.crud.crud_book import CRUDBook
from sqlalchemy.orm import Session

import pytest
from app.models.book import Book


from datetime import date
from app.crud.crud_book_plain import *
from unittest.mock import MagicMock
from app.models.author import Author
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from app.crud.crud_book_mongo import CRUDBookMongo
from app.crud.crud_book import CRUDBook  # Assuming this CRUDBook is compatible with MongoDB now


# Mock the Book class to have the new to_mongo method for serialization.
Book.to_mongo = staticmethod(to_mongo)


@pytest.fixture
def db():
    """Fixture to create a mock MongoDB collection."""
    return MagicMock()


# Assuming that 'db' fixture is a PyMongo collection now and 'crud_book' is adapted for MongoDB
def test_get_books_with_id_with_invalid_id(db: Collection, crud_book: CRUDBook):
    # In PyMongo, there isn't an "invalid" id concept like in SQL (-1), so let's use a dummy non-existing ObjectID
    invalid_id = '000000000000000000000000'
    assert crud_book.get_books_with_id(db, invalid_id) is None


# We create a new fixture for a dummy book dictionary since MongoDB works with dictionaries (BSON) instead of ORM models
@pytest.fixture
def dummy_book() -> dict:
    """Fixture to create a mock book without inserting it into the database."""
    book = {
        # MongoDB auto-generates an '_id', so we exclude that here
        'title': "Test Book",
        'pages': 123,
        'author_id': 1,
        'created_at': datetime(2020, 1, 1)
    }
    return book



def test_get_books_with_id_returns_correct_book(mongo_collection: Collection, dummy_book: DummyBook, crud_book: CRUDBookMongo):
    # Assuming mongo_collection represents the "books" collection in the MongoDB
    # Simulate a MongoDB document
    mongo_collection.find_one.return_value = {'_id': dummy_book.id, 'title': dummy_book.title, 'pages': dummy_book.pages}

    # When calling the get_book_by_id method, it should return the dummy book
    book = crud_book.get_book_by_id(mongo_collection, dummy_book.id)
    
    # Assert if the returned book instance matches the dummy book
    assert str(book['_id']) == str(dummy_book.id)
    assert book['title'] == dummy_book.title
    assert book['pages'] == dummy_book.pages


@pytest.fixture
def crud_book() -> CRUDBook:
    return CRUDBook()



def test_get_books_with_id_does_not_throw(
    db: DummyDatabase, dummy_book: Book, crud_book: CRUDBook
):
    book_id = ObjectId()

    # Prepare the mock for the find_one method of the books collection
    db.books.find_one = MagicMock(return_value=dummy_book.to_mongo())

    # Call the method with the mocked db and verify it does not throw
    result = crud_book.get_books_with_id(db, book_id)
    assert result is not None


# Assuming a to_mongo() method on the Book model to convert it to a dictionary for pymongo.
# You would need to add this to the Book class or use an equivalent way to serialize it.
def to_mongo(book: Book) -> dict:
    return {
        "_id": book.id,  # Assuming the Book model has an id attribute
        # ... Add the rest of the fields as needed
    }
