import pytest
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate
from app.models.book import Book
from app.crud.crud_book import *


# fixture to create book data
@pytest.fixture
def book_data():
    return BookCreate(title="Test Book", pages=100, author_id=1)


# fixture for creating an instance of CRUDBook class
@pytest.fixture
def crud_book():
    from app.database.CRUDBook import CRUDBook

    return CRUDBook()


# test that the function doesn't throw errors when it's executed
def test_create(db_session: Session, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj is not None


# test if created book has correct title
def test_create_title(db_session: Session, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj.title == "Test Book"


# test if created book has correct pages number
def test_create_pages(db_session: Session, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj.pages == 100


# test if created book has correct author id
def test_create_author_id(db_session: Session, crud_book, book_data: BookCreate):
    book_obj = crud_book.create(db=db_session, obj_in=book_data)
    assert book_obj.author_id == 1
