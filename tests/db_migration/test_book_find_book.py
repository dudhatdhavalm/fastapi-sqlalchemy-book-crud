#
#
#from datetime import date
#from fastapi.testclient import TestClient
#from sqlalchemy import create_engine
#from app.main import app  # Import the FastAPI app from the main script
#
#from app.api.dependencies import get_db
#from fastapi import FastAPI
#from typing import Generator
#from sqlalchemy.exc import OperationalError
#
#import pytest
#from sqlalchemy.orm import sessionmaker
#from app.models.book import Base, Book
#from app.api.endpoints.book import *
#import pytest
#
## Constants for database connection
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#client = TestClient(app)
#
#
#@pytest.fixture(scope="function")
#def db_session():
#    connection = engine.connect()
#    transaction = connection.begin()
#    session = TestingSessionLocal(bind=connection)
#    yield session
#
#    session.close()
#    connection.close()
#
#
#@pytest.fixture(scope="module")
#def temp_db():
#    Base.metadata.create_all(bind=engine)  # Create tables
#    _db = TestingSessionLocal()
#    try:
#        yield _db
#    finally:
#        _db.close()
#        Base.metadata.drop_all(bind=engine)  # Drop tables after the tests
#
#
#@pytest.fixture(scope="module")
#def client_with_db(temp_db):
#    # Dependency override for the database
#    def override_get_db():
#        try:
#            yield temp_db
#        finally:
#            temp_db.close()
#
#    app.dependency_overrides[get_db] = override_get_db
#    yield client  # use the client with the overridden dependency
#
#
#@pytest.fixture(scope="function")
#def create_sample_book(temp_db):
#    book = Book(title="Sample Book", published_date=date.today(), pages=123)
#    temp_db.add(book)
#    temp_db.commit()
#    temp_db.refresh(book)
#    return book
#
#
#def test_find_book_exists(db_session, client_with_db, create_sample_book):
#    # Test that find_book returns a valid response for an existing book
#    book = create_sample_book
#    response = client_with_db.get(f"/books/{book.id}")
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
#def test_find_book_does_not_exist(client_with_db):
#    # Test that find_book returns an appropriate response for a non-existing book
#    nonexistent_book_id = 99999
#    response = client_with_db.get(f"/books/{nonexistent_book_id}")
#    assert response.status_code == 404
#