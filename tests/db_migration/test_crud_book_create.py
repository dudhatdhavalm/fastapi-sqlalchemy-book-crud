#from sqlalchemy.orm import Session, sessionmaker
#from app.crud.crud_book import CRUDBook
#from app.db.base_class import Base
#
#
#from typing import TypeVar
#
#from app.crud.base import CRUDBase
#from app.models.book import Book
#from sqlalchemy import create_engine
#from app.models.author import Author
#
#import pytest
#from app.schemas.book import BookCreate
#
#
#import pytest
#from app.crud.crud_book import *
#from datetime import date
#
#from app.db.base_class import Base
#from sqlalchemy.orm import Session
#
## Assuming T is for our Book model
#T = TypeVar("T", bound=Base)
#
#
#class CRUDBook(CRUDBase[Book, BookCreate, BookCreate]):
#    def create(self, db: Session, *, obj_in: BookCreate) -> Book:
#        db_obj = super().create(db, obj_in=obj_in)
#        db_obj.created_at = date.today()
#        db.add(db_obj)
#        db.commit()
#        db.refresh(db_obj)
#        return db_obj
#
#    def __init__(self, model: T):
#        super().__init__(model)
#
#
## Creating an instance of CRUDBook for testing
#@pytest.fixture(scope="module")
#def crud_book(db_session: Session) -> CRUDBook:
#    return CRUDBook(Book)
#
#
#@pytest.fixture(scope="module")
#def db_session() -> Session:
#    # Define the database connection string
#    DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
#    # Set up the database engine
#    engine = create_engine(DATABASE_URL)
#    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    # Create the session
#    session = TestingSessionLocal()
#    # Create the database schema
#    Base.metadata.create_all(engine)
#    try:
#        yield session
#    finally:
#        session.rollback()
#        session.close()
#
#
## Test to check if the create method doesn't throw errors when executed
#def test_create_method_execution(db_session: Session, crud_book: CRUDBook):
#    test_author = Author(name="Test Author")
#    db_session.add(test_author)
#    db_session.commit()
#
#    book_data = BookCreate(title="Test Book", pages=123, author_id=test_author.id)
#    result = crud_book.create(db=db_session, obj_in=book_data)
#
#    assert result is not None, "The `create` method should return a non-None result."
#
#    # Cleanup: delete test author and book after the test run
#    db_session.delete(result)
#    db_session.delete(test_author)
#    db_session.commit()
#
## Import TypeVar for generic type annotation
#T = TypeVar("T", bound=Base)
#