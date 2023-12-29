from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from app.crud.crud_book_plain import *

import pytest
from app.schemas.book import BookCreate
from app.models.book import Book


from datetime import date
from pymongo.collection import Collection
from app.crud.crud_book_mongo import CRUDBookMongo  # Assuming this is the pymongo-compatible class
from unittest.mock import MagicMock
from bson import ObjectId

from app.crud.crud_book_plain import CRUDBook
from app.crud.crud_book import CRUDBook  # Assume this is the pymongo version of CRUD operations for 'Book'
from unittest.mock import Mock


@pytest.fixture
def mock_db_session():
    session = create_autospec(Session, instance=True)
    return session


# Test function

def test_create_with_no_title_raises_error(mock_db_session):
    """
    Test that CRUDBook.create method raises validation error when 'title' is not provided.
    """
    with pytest.raises(ValueError):
        crud_book = CRUDBook()
        # Assuming that the title field is necessary to create a book document in MongoDB
        # The 'mock_db_session' is assumed to be a MagicMock object simulating pymongo's database session
        crud_book.create(db=mock_db_session, obj_in=BookCreate(pages=123, author_id=1))


def test_create_with_no_author_id_raises_error(mock_db_collection):
    """
    Test that CRUDBook.create method raises validation error when 'author_id' is not provided.
    """
    with pytest.raises(ValueError):
        crud_book = CRUDBook(collection=mock_db_collection)  # Assuming CRUDBook takes a collection as a parameter
        crud_book.create(obj_in=BookCreate(title="Test Title", pages=123))


@pytest.fixture
def book_create_data():
    return BookCreate(title="Test Title", pages=123, author_id=1)


def test_create_book_instance(mock_db, book_create_data):
    """
    Test that CRUDBook.create method creates a book instance correctly using PyMongo.
    """
    # Mock the collection insert_one operation
    mock_collection = mock_db.get_collection('books')
    mock_collection.insert_one = MagicMock()

    # Create an example of the input data dictionary, mimicking PyMongo's behavior
    example_inserted_id = ObjectId()
    mock_collection.insert_one.return_value.inserted_id = example_inserted_id
    
    # Mock the collection find_one operation to return the book data after creation
    mock_collection.find_one = MagicMock(return_value={
        "_id": example_inserted_id,
        "title": book_create_data.title,
        "pages": book_create_data.pages,
        "author_id": book_create_data.author_id,
        # Add other fields as needed
    })

    crud_book = CRUDBook(collection=mock_collection)
    book = crud_book.create(obj_in=book_create_data)

    # Assert that insert_one operation was called correctly
    mock_collection.insert_one.assert_called_once_with({
        "title": book_create_data.title,
        "pages": book_create_data.pages,
        "author_id": book_create_data.author_id,
        # Add other fields as needed
    })

    # Assert that the book instance is created with the correct data
    assert book.title == book_create_data.title
    assert book.pages == book_create_data.pages
    assert book.author_id == book_create_data.author_id


@pytest.fixture
def book_instance():
    return Book(title="Test Title", pages=123, author_id=1)


# Import statements for mock_db_collection, book_create_data, and other fixtures should be here
# ...


def test_create_does_not_raise_error(mock_db_collection, book_create_data):
    """
    Test that the CRUDBookMongo.create method does not raise an error
    when called with valid arguments.
    """
    crud_book = CRUDBookMongo()
    result = crud_book.create(db=mock_db_collection, obj_in=book_create_data)

    # In PyMongo, the insert operation returns an InsertOneResult which contains the inserted_id
    assert result is not None
    assert result.inserted_id is not None

# The fixtures functions would be using Pytest fixtures and would look like this:

@pytest.fixture
def mock_db_collection():
    mock_collection = create_autospec(Collection)
    return mock_collection


def test_create_book_date_set(mock_db_session, book_create_data):
    """
    Test that CRUDBook.create method sets the created_at date.
    """
    crud_book = CRUDBook()
    book = crud_book.create(db=mock_db_session, obj_in=book_create_data)

    assert book.created_at is not None
