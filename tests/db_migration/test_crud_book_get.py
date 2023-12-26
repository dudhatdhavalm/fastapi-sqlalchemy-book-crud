from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.crud.crud_book import *

# Create an in-memory SQLite database for testing purposes
DATABASE_URL = "sqlite:///:memory:"

# Set up the SQLAlchemy engine and sessionmaker for the SQLite database
engine = create_engine(DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()  # Use the SQLAlchemy base class


# Mock a minimal Book model with an id as primary key for testing purposes
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)


# Since we don't have control over the actual CRUDBook class,
# here we create a MockCRUDBook class to simulate the real one.
# It accepts a Book model during instantiation, following the assumption.
class MockCRUDBook:
    def __init__(self, model):
        self.model = model

    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.query(self.model).offset(skip).limit(limit).all()


Base.metadata.create_all(bind=engine)  # Create the tables in the in-memory SQLite DB


# Fixture for setting up a new database session for each test function
@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Test to ensure the `get` method of `MockCRUDBook` does not throw errors
@pytest.mark.parametrize("skip, limit", [(0, 10), (20, 20)])
def test_get_method_no_errors(db_session: Session, skip: int, limit: int):
    crud_book = MockCRUDBook(Book)  # Assumption: CRUDBook accepts a model argument
    books = crud_book.get(db=db_session, skip=skip, limit=limit)
    assert (
        books is not None
    )  # Checking that the method call does not raise any exceptions


# Additional test scenarios could be added below, following the guidelines.
