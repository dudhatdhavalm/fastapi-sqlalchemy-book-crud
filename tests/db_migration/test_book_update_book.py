#from fastapi.testclient import TestClient
#from sqlalchemy.orm import Session
#from app.api.endpoints.book import *
#from sqlalchemy.orm import sessionmaker
#
#import pytest
#from datetime import date
#
#from app.api.dependencies import get_db
#from app.main import app
#from app.models.book import Book
#
#
#from sqlalchemy import create_engine
#
## Setup the database and session for the tests
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base.metadata.create_all(bind=engine)
#
#
#def override_get_db():
#    try:
#        db = TestingSessionLocal()
#        yield db
#    finally:
#        db.close()
#
#
#app.dependency_overrides[get_db] = override_get_db
#client = TestClient(app)
#
#
#@pytest.fixture(scope="function")
#def db_session():
#    db = TestingSessionLocal()
#    yield db
#    db.close()
#
#
#@pytest.fixture(scope="function")
#def test_book(db_session) -> Book:
#    book = Book(title="Test Book", author_id=1, publish_date=date.today())
#    db_session.add(book)
#    db_session.commit()
#    db_session.refresh(book)
#    return book
#
#
#def test_update_book_no_error(test_book):
#    response = client.put(
#        f"/books/{test_book.id}",
#        json={
#            "title": "Updated Test Book",
#            "author_id": test_book.author_id,
#            "publish_date": test_book.publish_date.isoformat(),
#        },
#    )
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
#def test_update_book_not_found():
#    nonexistent_book_id = (
#        99999  # We're using a high number to assume it does not exist.
#    )
#    response = client.put(
#        f"/books/{nonexistent_book_id}",
#        json={
#            "title": "Nonexistent Book",
#            "author_id": 1,
#            "publish_date": date.today().isoformat(),
#        },
#    )
#    assert response.status_code == 404
#
#
#def test_update_book_author_not_found(test_book):
#    nonexistent_author_id = (
#        99999  # We're using a high number to assume it does not exist.
#    )
#    response = client.put(
#        f"/books/{test_book.id}",
#        json={
#            "title": "Book with Nonexistent Author",
#            "author_id": nonexistent_author_id,
#            "publish_date": date.today().isoformat(),
#        },
#    )
#    assert response.status_code == 404
#