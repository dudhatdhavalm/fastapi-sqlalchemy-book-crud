import pytest
from app.crud.crud_book import *

from sqlalchemy import create_engine
from app.models.author import Author


from datetime import date
from sqlalchemy.orm import Session
from app.models.book import Book


# fixture to setup and teardown a session
@pytest.fixture
def session():
    engine = create_engine("postgresql://localhost/BooksDB")
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    # teardown
    session.close()
    transaction.rollback()
    connection.close()
    engine.dispose()


# fixture to setup and teardown some test data
@pytest.fixture
def test_data(session):
    # setup
    author1 = Author(id=1, name="Author1")
    session.add(author1)
    book1 = Book(id=1, title="Book1", pages=100, created_at=date.today(), author_id=1)
    session.add(book1)
    session.commit()
    # yield data for test to use
    yield {"author": author1, "book": book1}
    # teardown
    session.query(Book).delete()
    session.query(Author).delete()
    session.commit()


def test_get_with_author(session, test_data):
    crudbook = CRUDBook()
    books = crudbook.get_with_author(session)
    # check returned books have correct format
    for book in books:
        assert isinstance(book["id"], int)
        assert isinstance(book["title"], str)
        assert isinstance(book["pages"], int)
        assert isinstance(book["created_at"], date)
        assert isinstance(book["author_id"], int)
        assert isinstance(book["author_name"], str)
    # check returned books include test data
    assert any(book["id"] == test_data["book"].id for book in books)
    assert any(book["author_name"] == test_data["author"].name for book in books)
