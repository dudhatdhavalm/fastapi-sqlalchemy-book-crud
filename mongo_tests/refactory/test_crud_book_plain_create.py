from app.crud.crud_book_plain import *
import pytest
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate
from app.models.book import Book
from pymongo.collection import Collection
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId





# fixture to create book data
@pytest.fixture
def book_data():
    return {"title": "Test Book", "pages": 100, "author_id": 1}


def test_create_pages(mongo_client: MongoClient, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=mongo_client.test_db, obj_in=book_data)
    assert book_obj.pages == 100





# test if created book has correct author id
def test_create_author_id(mongo_client: MongoClient, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(client=mongo_client, obj_in=book_data)
    assert book_obj.author_id == 1


# test that the function doesn't throw errors when it's executed
def test_create(db_session: MongoClient, book_data: dict):
    book_obj = db_session.test_db.books.insert_one(book_data)
    assert book_obj is not None


# test if created book has correct title
def test_create_title(db_session: pymongo.MongoClient, book_data: BookCreate):
    # Assuming crud_book.create adds a book to a "books" collection in MongoDB
    books = db_session["database"]["books"]
    book_obj_id = books.insert_one(vars(book_data)).inserted_id

    # Fetch the newly added book document
    book_obj = books.find_one({"_id": ObjectId(book_obj_id)})

    # Verify the correct title
    assert book_obj["title"] == "Test Book"



# Fixture for creating an instance of CRUDBook class
@pytest.fixture
def crud_book():
    from app.database.CRUDBook import CRUDBook

    return CRUDBook()


# Fixture for creating pymongo client instance to connect with MongoDB
@pytest.fixture
def db_session():
    client = MongoClient('localhost', 27017)
    db = client['test_database']
    return db
