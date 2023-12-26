#import pytest
#from sqlalchemy.orm import sessionmaker
#from app.api.endpoints.book import *
#from fastapi.testclient import TestClient
#from sqlmodel import Session, SQLModel
#
#from app.api.dependencies import get_db
#from app.models.book import Base, Book
#
#
#from typing import Callable, Generator
#
#from fastapi import FastAPI, status
#from fastapi import FastAPI, status
#from sqlalchemy import create_engine
#
## Constants for test data
#EXISTING_BOOK_ID = 1
#NON_EXISTING_BOOK_ID = 999
#
## Using the specified database URL for testing
#TEST_DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703603283683"
#test_engine = create_engine(TEST_DATABASE_URL)
#
#
#@pytest.fixture(name="client")
#def fixture_client() -> TestClient:
#    app = FastAPI()
#    app.include_router(router)
#    client = TestClient(app)
#    return client
#
#
#@pytest.fixture(name="test_db")
#def fixture_test_db() -> Generator:
#    # Bind the engine to the Session class
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
#    # Create the database session and tables
#    Base.metadata.create_all(bind=test_engine)
#    db = SessionLocal()
#    # Pre-populate the test database
#    db.add(Book(id=EXISTING_BOOK_ID, title="Test book", author="John Doe"))
#    db.commit()
#    try:
#        yield db
#    finally:
#        db.close()
#        Base.metadata.drop_all(bind=test_engine)
#
#
#@pytest.fixture(name="override_get_db")
#def fixture_override_get_db(test_db) -> Callable:
#    def override_test_db():
#        return test_db
#
#    app.dependency_overrides[get_db] = override_test_db
#    yield
#    app.dependency_overrides.clear()
#
#
#def test_get_by_id_does_not_raise_errors(client: TestClient, override_get_db: Callable):
#    response = client.get(f"/book/{EXISTING_BOOK_ID}")
#    assert response.status_code == status.HTTP_200_OK
#    assert response.json() is not None
#
#
#def test_get_by_id_book_not_found(client: TestClient, override_get_db: Callable):
#    response = client.get(f"/book/{NON_EXISTING_BOOK_ID}")
#    assert response.status_code == status.HTTP_404_NOT_FOUND
#    assert "not found" in response.json().get("detail", "")
#