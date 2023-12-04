#from typing import Any, Dict, TypeVar
#
#import pytest
#from sqlalchemy import create_engine
#from app.models.book import Book
#from app.models.author import Author
#from app.crud.crud_book import *
#
#
#from datetime import date
#from sqlalchemy.orm import Session, sessionmaker
#from datetime import date
#
#T = TypeVar("T", bound=CRUDBook)
#
#
#class TestCRUDBook:
#    @staticmethod
#    def setup_method():
#        SQLALCHEMY_DATABASE_URL = (
#            "postgres://root:postgres@localhost:5432/code_robotics_1701690361803"
#        )
#        engine = create_engine(SQLALCHEMY_DATABASE_URL)
#        SessionLocal = sessionmaker(bind=engine)
#
#        db = SessionLocal()
#        book_info = {"id": 1, "title": "Test Book Title", "pages": 360, "author_id": 1}
#        author_info = {"id": 1, "name": "Test Author"}
#        db.add(Author(**author_info))
#        db.add(Book(**book_info))
#        db.commit()
#
#    def test_get_books_with_id(self):
#        SQLALCHEMY_DATABASE_URL = (
#            "postgres://root:postgres@localhost:5432/code_robotics_1701690361803"
#        )
#        engine = create_engine(SQLALCHEMY_DATABASE_URL)
#        SessionLocal = sessionmaker(bind=engine)
#
#        db = SessionLocal()
#
#        book = CRUDBook.get_books_with_id(db, 1)
#        assert book is not None
#
#
#@pytest.mark.parametrize("book_id", [-1, "abcd"])
#def test_get_books_with_id_not_exists(book_id: int):
#    SQLALCHEMY_DATABASE_URL = (
#        "postgres://root:postgres@localhost:5432/code_robotics_1701690361803"
#    )
#    engine = create_engine(SQLALCHEMY_DATABASE_URL)
#    SessionLocal = sessionmaker(bind=engine)
#
#    db = SessionLocal()
#
#    book = CRUDBook.get_books_with_id(db, book_id)
#    assert book is None
#