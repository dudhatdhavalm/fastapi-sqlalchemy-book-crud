from app.crud.crud_book_plain import *
import pytest
from sqlalchemy.orm import Session
from app.models.author import Author
from app.models.book import Book
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.errors import OperationFailure

# Define client and database globally
client = MongoClient('localhost', 27017)


def test_update(db, db_book, update_book):
    crud_book = CRUDBook()
    updated_book_id = crud_book.update(db, db_obj=db_book['_id'], obj_in=update_book)
    
    updated_book = db['books'].find_one({"_id": ObjectId(updated_book_id)}) # Fetch the updated record
    assert updated_book is not None
    assert updated_book['title'] == "Updated Test Book"
    assert updated_book['year'] == "2021"
    assert updated_book['author_id'] == 1
    assert isinstance(updated_book['created_at'], datetime)
    assert updated_book['created_at'].date() == datetime.today().date()



def test_update_with_no_valid_obj_in(db, db_book):
    crud_book = CRUDBook()
    try:
        crud_book.update(db, db_obj=db_book, obj_in=None)
    except Exception as e:
        assert isinstance(e, TypeError)



def test_update_with_no_valid_db_obj(db, update_book):
    crud_book = CRUDBook()
    try:
        crud_book.update(db, db_obj=None, obj_in=update_book)
    except Exception as e:
        assert isinstance(e, OperationFailure)
db = client.test_database


# Define fixtures for MongoDB
@pytest.fixture
def update_book():
    return {"title": "Updated Test Book", "year": "2021", "author_id": 1}

# expected to be set externally
client = MongoClient('mongo_url')  
db = client['db_name']  


@pytest.fixture(scope="function")
def db():
    client = MongoClient()
    db = client.test_database
    yield db
    client.close()


@pytest.fixture
def db_book():
    new_book_id = db.books.insert_one({"title": "Test Book", "year": "2020", "author_id": ObjectId(), "created_at": datetime.utcnow()}).inserted_id
    book = db.books.find_one({"_id": new_book_id})
    yield book
    db.books.delete_one({"_id": new_book_id}) 
