from sqlalchemy.orm import Session, sessionmaker
from app.models.book import Book
from sqlalchemy import create_engine
import pytest

from app.crud.crud_book_plain import *
from app.schemas.book import BookCreate
from app.db.base_class import Base

# Set up an in-memory SQLite database for testing purposes
# We will use SQLite for testing instead of the production Postgres database
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Set up a fixture to provide a database session for the tests
@pytest.fixture(scope="module")
def db_session():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new database session for a test
    db_session = TestingSessionLocal()

    # Run the test
    yield db_session

    # Close the session
    db_session.close()

    # Drop all data after tests complete
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def book_create_payload():
    return BookCreate(title="Test Book", pages=123, author_id=1)


# Test to ensure the create method doesn't throw errors when executed
def test_create_book_without_errors(
    db_session: Session, book_create_payload: BookCreate
):
    crud_book = CRUDBook()
    result = crud_book.create(db=db_session, obj_in=book_create_payload)
    assert (
        result is not None
    ), "The create method should return a Book instance, not None"


# Add more tests for edge cases below...

# Ensure imports from the file that is tested don't have to be included
# (because they are already in scope, according to the instructions)


from app.crud.crud_book_plain import CRUDBook
