import pytest
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate
from app.models.book import Book
from app.crud.crud_book import *
from pymongo import MongoClient
from bson import ObjectId
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo.collection import ReturnDocument



# test if created book has correct pages number
def test_create_pages(db_session: MongoClient, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj.pages == 100



# test if created book has correct author id
def test_create_author_id(db_session: MongoClient, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj['author_id'] == 1



# test if created book has correct title
def test_create_title(db, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db, obj_in=book_data.dict())
    retrieved_book = db.books.find_one({"_id": book_obj.inserted_id})
    assert retrieved_book['title'] == "Test Book"


    

# test that the function doesn't throw errors when it's executed
def test_create(db_session: MongoClient, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj is not None

# PyMongo setup
client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']
book_collection = db['book']


# fixture for creating an instance of CRUDBook class
@pytest.fixture
def crud_book():
    from app.database.CRUDBook import CRUDBook
    return CRUDBook()

db = MongoClient().test_database


# Fixture to create book data
@pytest.fixture
def book_data():
    return {"title": "Test Book", "pages": 100, "author_id": ObjectId()}
