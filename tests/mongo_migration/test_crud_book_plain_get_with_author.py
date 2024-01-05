import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

from app.crud.crud_book_plain import *


from datetime import date
from pymongo import MongoClient
from datetime import datetime



def test_get_with_author_correct_mapping(mongo_session):
    crud_book = CRUDBook()
    books_with_authors = crud_book.get_with_author(mongo_session)

    assert len(books_with_authors) == 2, "There should be two books with authors in the result."
    assert books_with_authors[0]['author_name'] == "Author One", "The author name should be correctly mapped in the result."


# Import any required methods and classes here

@pytest.fixture
def db_session():
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    db = client['test_db']
    
    # Drop the collection in case it already exists, to start fresh
    db.drop_collection('books')

    # Create a mock collection
    mock_collection = db['books']

    mock_query_result = [
        {
            "_id": 1,  # Assuming numerical IDs are used, otherwise ObjectId should be used
            "title": "Book One",
            "pages": 100,
            "created_at": datetime(2021, 5, 21),
            "author_id": 1,
            "author_name": "Author One",
        },
        {
            "_id": 2,
            "title": "Book Two",
            "pages": 200,
            "created_at": datetime(2021, 6, 21),
            "author_id": 2,
            "author_name": "Author Two",
        },
    ]
    
    # Insert the mock data into the collection
    mock_collection.insert_many(mock_query_result)
    
    # Return a mock database session
    return mock_collection


# Assuming that mongo_session is a fixture that sets up a connection to the MongoDB database
@pytest.fixture
def mongo_session():
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    db = client['code_robotics_1704487699809']
    yield db
    # Add any teardown steps if necessary, such as dropping the test database
    client.close()


def test_get_with_author_no_errors(db_session):
    crud_book = CRUDBook()
    result = crud_book.get_with_author(db_session)
    assert result is not None, "The function should return a value."


def test_get_with_author_author_id(db_session):
    crud_book = CRUDBook()
    books_with_authors = crud_book.get_with_author(db_session)
    assert (
        books_with_authors[0].author_id == 1
    ), "The author ID should be correctly mapped in the result."
