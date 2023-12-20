#from fastapi.testclient import TestClient
#from app.dependencies import get_db
#from app.api.endpoints.book import *
#from app.schemas.book import Books
#import pytest
#from sqlalchemy.orm import Session
#
#client = TestClient(app)
#
#
#@pytest.fixture
#def test_get_book_id(db: Session):
#    # Here, we prepare test data
#    data = Books(
#        title="Test book", author="Test Author", description="Test Description"
#    )
#    db.add(data)
#    db.commit()
#    db.refresh(data)
#    return data.id
#
#
#def test_get_by_id(test_get_book_id: int, db: Session = get_db):
#    response = client.get(f"/{test_get_book_id}")
#    assert response.status_code == 200
#    assert response.json() != None
#    assert isinstance(response.json(), dict)
#    assert "title" in response.json()
#    assert "author" in response.json()
#    assert "description" in response.json()
#
#
#def test_get_by_id_not_present():
#    non_existent_id = 999  # an id that does not exist in the database
#    response = client.get(f"/{non_existent_id}")
#    assert response.status_code == 404
#
#
#def test_get_by_id_invalid():
#    invalid_id = "abcd"  # an invalid id that is not an integer
#    response = client.get(f"/{invalid_id}")
#    assert response.status_code == 422  # Unprocessable Entity
#