#from app.models.book import Book
#from app.schemas.book import BookCreate
#
#import pytest
#from unittest.mock import MagicMock
#from datetime import date
#
#from app.crud.crud_book import *
#
#
#from datetime import date
#from sqlalchemy.orm import Session
#
#
## Create a fake DB session for testing
#@pytest.fixture(scope="module")
#def fake_db_session() -> Session:
#    fake_session = MagicMock()
#    fake_session.commit = MagicMock()
#    fake_session.refresh = MagicMock()
#    fake_session.add = MagicMock()
#    return fake_session
#
#
#@pytest.fixture(scope="module")
#def book_create() -> BookCreate:
#    return BookCreate(title="Test Book", pages=123, author_id=1)
#
#
#@pytest.fixture(scope="module")
#def crud_book() -> CRUDBook:
#    return CRUDBook()
#
#
#def test_create_no_errors(
#    crud_book: CRUDBook, fake_db_session: Session, book_create: BookCreate
#):
#    try:
#        crud_book.create(db=fake_db_session, obj_in=book_create)
#    except Exception as e:
#        pytest.fail(f"An error occurred: {e}")
#
#
#def test_create_returns_book_instance(
#    crud_book: CRUDBook, fake_db_session: Session, book_create: BookCreate
#):
#    book = crud_book.create(db=fake_db_session, obj_in=book_create)
#    assert isinstance(book, Book)
#
#
#def test_create_sets_created_at_to_today(
#    crud_book: CRUDBook, fake_db_session: Session, book_create: BookCreate
#):
#    fake_db_session.refresh = MagicMock(
#        side_effect=lambda obj: setattr(obj, "created_at", date.today())
#    )
#    book = crud_book.create(db=fake_db_session, obj_in=book_create)
#    assert isinstance(book.created_at, date)
#    assert book.created_at == date.today()
#
#
#def test_create_commits_session(
#    crud_book: CRUDBook, fake_db_session: Session, book_create: BookCreate
#):
#    crud_book.create(db=fake_db_session, obj_in=book_create)
#    fake_db_session.commit.assert_called_once()
#
#
#def test_create_adds_book_to_session(
#    crud_book: CRUDBook, fake_db_session: Session, book_create: BookCreate
#):
#    crud_book.create(db=fake_db_session, obj_in=book_create)
#    fake_db_session.add.assert_called_once()
#