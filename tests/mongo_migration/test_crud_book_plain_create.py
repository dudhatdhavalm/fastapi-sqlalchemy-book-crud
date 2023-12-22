from datetime import date
from app.db.base_class import Base
from app.models.book import Book

from app.crud.crud_book_plain import *
from sqlalchemy import create_engine

import pytest
from sqlalchemy.orm import sessionmaker
from app.schemas.book import BookCreate

from app.crud.crud_book_plain import CRUDBook
from datetime import date
from app.crud.crud_book_plain import CRUDBook
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pymongo.collection import Collection
from app.crud.crud_book_plain import CRUDBook  # Assuming CRUDBook is implemented for MongoDB
from app.schemas.book import BookCreate  # You might need a different schema suitable for MongoDB

ENGINE_URL = (
    "sqlite:///:memory:"  # For testing purposes, using an in-memory SQLite database
)
engine = create_engine(ENGINE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Assuming 'BookCreate' would translate to a simple dictionary in PyMongo context
# and we build our functions accordingly.

@pytest.fixture(scope="function")
def book_data():
    # MongoDB uses '_id' as the default primary key, which is automatically generated.
    # We can still define 'title', 'pages', and 'author_id' as in the original fixture.
    return {"title": "Test Book", "pages": 123, "author_id": ObjectId()}


# Assuming that 'crud_book' is an adapted version of the CRUD class for pymongo
# and that 'book_data' is a fixture providing a dictionary with book information.

def test_create_book_correct_pages(crud_book, db_client, book_data):
    book_collection = db_client['your_database_name']['book_collection']
    
    # The 'create' method would insert the data directly into MongoDB
    # and would return the inserted_id or the complete inserted document based on implementation
    result = crud_book.create(book_collection, obj_in=book_data)

    # If the create method returns just inserted_id, we need to get the full document
    if isinstance(result, ObjectId):
        book = book_collection.find_one({'_id': result})
    else:
        book = result
    
    assert book['pages'] == 123


# In the scope, we assume that db_session() now returns a pymongo collection
# and a book_data() fixture provides a dictionary with book data ready to insert into MongoDB

def test_create_no_errors(crud_book, db_session, book_data):
    # CRUDBook.create should insert the document into the database
    # and return the inserted document, including the auto-generated '_id' field by MongoDB
    result = crud_book.create(db_session, obj_in=book_data)
    assert result is not None
    assert result.inserted_id is not None  # We check that an '_id' field was created on insertion

    # Clean up the inserted document after the test
    db_session.delete_one({'_id': result.inserted_id})


# Assume 'mongo_client' and 'book_data' are defined elsewhere in your test suite

def test_create_book_correct_created_at(crud_book_mongo, mongo_client, book_data):
    # Given a PyMongo CRUDBookMongo instance, a MongoClient, and the book_data dictionary
    
    # Assume a database named 'testdb' and a collection named 'books' for this example
    collection = mongo_client.testdb.books
    crud_book = CRUDBookMongo(collection)
    
    # When creating a new book document
    book = crud_book.create(book_data)
    
    # Then the created_at date should be correct
    assert book['created_at'] == date.today()

# Fixture function providing the database client used in the test cases
@pytest.fixture(scope='module')
def db_client():
    client = MongoClient("mongodb://localhost:27017/")
    yield client
    client.close()
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def mongo_collection(mongodb):
    return mongodb.get_collection('books')


# Import your book document schema, usually using a class or a dictionary
# For this example, it's assumed you use a dictionary to define the schema
# from app.models.book import Book as BookDocument

@pytest.fixture(scope="function")
def db_session():
    client = MongoClient('localhost', 27017)  # Connect to your MongoDB instance
    db = client.test_database  # Use a test database

    yield db

    # Teardown: drop the test database
    client.drop_database('test_database')
    client.close()


@pytest.fixture(scope="function")
def crud_book():
    return CRUDBook()


def test_create_book_correct_title(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.title == "Test Book"


def test_create_book_correct_author_id(crud_book, db_session, book_data):
    book = crud_book.create(db_session, obj_in=book_data)
    assert book.author_id == 1
