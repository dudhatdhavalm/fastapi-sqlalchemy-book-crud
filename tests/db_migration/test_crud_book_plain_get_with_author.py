#
#import pytest
#from app.db.base_class import Base
#from app.crud.crud_book_plain import CRUDBook
#from sqlalchemy import create_engine
#from app.crud.crud_book_plain import *
#from app.models.book import Book
#from app.models.author import Author
#from sqlalchemy.orm import Session, sessionmaker
#from datetime import date
#
#
#@pytest.fixture
#def test_db_session():
#    SQLALCHEMY_DATABASE_URL = (
#        "postgresql://root:postgres@localhost:5432/code_robotics_1701690361803"
#    )
#    engine = create_engine(SQLALCHEMY_DATABASE_URL)
#    Base.metadata.create_all(bind=engine)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    session = SessionLocal()
#    yield session
#    session.close()
#
#
#@pytest.fixture
#def test_crud_book(test_db_session):
#    book_crud = CRUDBook(test_db_session)
#    yield book_crud
#
#
#def test_get_with_author(test_crud_book, test_db_session):
#    result = test_crud_book.get_with_author(test_db_session)
#    assert result is not None
#    assert all(isinstance(res, Book) for res in result)
#
#
#def test_get_with_author_returns_books(test_crud_book, test_db_session):
#    result = test_crud_book.get_with_author(test_db_session)
#    assert len(result) >= 1
#    assert all(isinstance(res, Book) for res in result)
#
#
#def test_get_with_author_empty_db(test_crud_book, test_db_session):
#    test_db_session.query(Book).delete()
#    result = test_crud_book.get_with_author(test_db_session)
#    assert result == []
#    assert all(isinstance(res, Book) for res in result)
#