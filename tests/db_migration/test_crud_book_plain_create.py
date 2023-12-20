#
#import pytest
#
#from sqlalchemy import create_engine
#from sqlalchemy import create_engine
#
#
#from typing import List
#from app.crud.crud_book_plain import *
#from app.models.book import Book
#from sqlalchemy.orm import sessionmaker
#from datetime import date
#from app.schemas.book import BookCreate
#
#engine = create_engine(
#    "postgresql://postgres:postgres@localhost/code_robotics_1701690361803"
#)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#@pytest.fixture
#def db():
#    # connect to the database
#    db = TestingSessionLocal()
#    yield db
#    # disconnect from the database
#    db.close()
#
#
#def test_create_book(db):
#    book_info = BookCreate(title="test title", pages=100, author_id=1)
#    crud_book = CRUDBook()
#    new_book = crud_book.create(db, obj_in=book_info)
#    assert new_book is not None
#    assert isinstance(new_book, Book)
#    assert new_book.title == "test title"
#    assert new_book.pages == 100
#    assert new_book.author_id == 1
#    assert new_book.created_at == date.today()
#