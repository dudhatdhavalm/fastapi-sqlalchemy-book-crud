#from datetime import datetime
#
#import pytest
#from fastapi.testclient import TestClient
#from app.models.book import Base
#
#
#from datetime import datetime
#from app.settings import DATABASE_URL
#from sqlalchemy import create_engine
#from app.api.endpoints.book import *
#from app import crud
#from sqlalchemy.orm import sessionmaker
#from app.schemas.book import BookCreate
#
#engine = create_engine(DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base.metadata.create_all(bind=engine)
#
#
#@pytest.fixture
#def db():
#    db = SessionLocal()
#    yield db
#    db.close()
#
#
#@pytest.fixture
#def client():
#    return TestClient(app)
#
#
#def test_get_book(db, client):
#    # Prepare book data
#    book = BookCreate(title="Test Book", author_id=1, publication_date=datetime.now())
#    # Create book in database
#    db_book = crud.book.create(db, obj_in=book)
#
#    # Execute Test
#    response = client.get("/book")
#
#    # Cleanup
#    db.delete(db_book)
#    db.commit()
#
#    # Test Assertions
#    assert response.status_code == 200
#    assert response.json() is not None
#