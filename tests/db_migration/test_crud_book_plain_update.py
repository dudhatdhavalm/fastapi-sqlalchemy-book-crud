#
#import pytest
#from app.crud.crud_book_plain import CRUDBook
#from fastapi.testclient import TestClient
#from app.schemas.book import BookCreate, BookUpdate
#from app.crud.crud_book_plain import *
#from app.db.session import SessionLocal
#from app.models.author import Author
#from app.models.book import Book
#
#
#from datetime import date
#
#from main import app
#from datetime import date
#from sqlalchemy.orm import Session
#
#client = TestClient(app)
#
#
#@pytest.fixture(scope="module")
#def test_app():
#    return app
#
#
#@pytest.fixture(scope="module")
#def db_session():
#    return SessionLocal()
#
#
#def create_test_author(db: Session, author_name="Test Author"):
#    new_author = Author(name=author_name)
#    db.add(new_author)
#    db.commit()
#    db.refresh(new_author)
#    return new_author
#
#
#def create_test_book(
#    db: Session,
#    book_title="Test Book",
#    author_id: int,
#    pages: int,
#    release_date=date.today(),
#):
#    book_in = BookCreate(
#        title=book_title, author_id=author_id, pages=pages, release_date=release_date
#    )
#    book = Book(**book_in.dict())
#    db.add(book)
#    db.commit()
#    db.refresh(book)
#    return book
#
#
#def test_update_no_errors(db_session):
#    author = create_test_author(db_session)
#    book = create_test_book(db_session, author_id=author.id, pages=100)
#    updated_data = BookUpdate(title="Updated Test Book", pages=100)
#    crud = CRUDBook()
#    updated_book = crud.update(db=db_session, db_obj=book, obj_in=updated_data)
#    assert updated_book is not None
#
#
#def test_update_fields(db_session):
#    author = create_test_author(db_session)
#    book = create_test_book(db_session, author_id=author.id, pages=100)
#    updated_data = BookUpdate(title="Updated Test Book", pages=100)
#    crud = CRUDBook()
#    updated_book = crud.update(db=db_session, db_obj=book, obj_in=updated_data)
#    assert updated_book.title == "Updated Test Book"
#    assert updated_book.release_date == book.release_date
#