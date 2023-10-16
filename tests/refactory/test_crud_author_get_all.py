from sqlalchemy.orm import Session as SqlalchemySession
import pytest
from sqlalchemy import create_engine
from app.crud.crud_author import *
from app.models.author import Author
from sqlalchemy.orm import sessionmaker

# global scope
engine = create_engine("postgresql://postgres:root@localhost:5432/BooksDB")


# creating pytest fixture for database session
@pytest.fixture
def db() -> Generator[SqlalchemySession, None, None]:
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# function to create a new author
def create_new_author(db: SqlalchemySession, name: str = "Test") -> Author:
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


# Now, we can start creating our tests


# first test is to ensure we are getting something (not none)
# and the function doesn't throw any error.
def test_get_all(db):
    crud_author = CRUDAuthor()
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert authors is not None


# Test to check if there are no authors in the database,
# get_all should return an empty list.
def test_get_all_no_authors(db):
    crud_author = CRUDAuthor()
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert authors == []


# test to check that the function correctly gets all authors if limit is more than number of authors
def test_get_all_more_limit(db):
    crud_author = CRUDAuthor()
    create_new_author(db)
    authors = crud_author.get_all(db, skip=0, limit=100)
    assert len(authors) == 1


# Test to check the function when the skip parameter is used.
def test_get_all_with_skip(db):
    crud_author = CRUDAuthor()
    create_new_author(db)
    create_new_author(db, name="Test2")
    authors = crud_author.get_all(db, skip=1, limit=100)
    assert len(authors) == 1


# Test to check that the function returns empty list if limit is 0
def test_get_all_limit_zero(db):
    crud_author = CRUDAuthor()
    create_new_author(db)
    authors = crud_author.get_all(db, skip=0, limit=0)
    assert authors == []
