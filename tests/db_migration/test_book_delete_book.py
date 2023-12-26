#
#from app.crud import book as crud_book
#
#
#from datetime import date
#from app.schemas.book import BookCreate
#import pytest
#
#import pytest
#from fastapi.testclient import TestClient
#from app.models.book import Base, Book
#from app.database import get_db
#from sqlalchemy.orm import Session, sessionmaker
#from app.crud import book as crud_book
#
#from app.api.endpoints.book import *
#from app.main import app
#from sqlalchemy import create_engine
#
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703603283683"
#client = TestClient(app)
#
#
#@pytest.fixture(scope="function")
#def db() -> Session:
#    engine = create_engine(DATABASE_URL)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    Base.metadata.create_all(bind=engine)
#    db_session = SessionLocal()
#    try:
#        yield db_session
#    finally:
#        db_session.close()
#
#
#@pytest.fixture(scope="function")
#def test_book(db: Session) -> Book:
#    book_data = BookCreate(
#        title="Test Book", author="Test Author", publication_date=date(2021, 1, 1)
#    )
#    book = crud_book.create(db=db, obj_in=book_data)
#    db.commit()
#    db.refresh(book)
#    yield book
#    crud_book.remove(db=db, id=book.id)
#
#
#def test_delete_book_no_errors(db: Session, test_book: Book):
#    # Testing if the delete_book function doesn't throw errors when it's executed
#    response = client.delete(f"/books/{test_book.id}")
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
#def test_delete_book_existing_id(db: Session, test_book: Book):
#    # Testing delete_book with an existing book ID should return a success message
#    book_id = test_book.id
#    response = client.delete(f"/books/{book_id}")
#    assert response.status_code == 200
#    result = response.json()
#    assert "detail" in result
#    assert result["detail"] == f"Book id {book_id} deleted successfully"
#
#
#def test_delete_book_invalid_id(db: Session):
#    # Testing delete_book with an invalid book ID should return 404 error
#    invalid_id = 999999
#    response = client.delete(f"/books/{invalid_id}")
#    assert response.status_code == 404
#