#from sqlalchemy.orm import sessionmaker
#
#from app.api.dependencies import get_db
#from app.main import app  # Assuming the FastAPI app is initialized in this module
#from sqlalchemy import create_engine
#import pytest
#
#
#from sqlalchemy.orm import Session
#from app.models.author import Author
#from fastapi.testclient import TestClient
#from app.api.endpoints.author import *
#
#
## Fixture to prepare the database for testing
#@pytest.fixture(scope="module")
#def test_db():
#    DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
#    engine = create_engine(DATABASE_URL)
#    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#    Base.metadata.create_all(bind=engine)
#    db = TestingSessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#
#
## Fixture to override the get_db dependency
#@pytest.fixture
#def override_get_db(test_db):
#    def _override_get_db():
#        return test_db
#
#    return _override_get_db
#
#
## Fixture to create a test client
#@pytest.fixture
#def client(override_get_db):
#    app.dependency_overrides[get_db] = override_get_db
#    with TestClient(app) as test_client:
#        yield test_client
#
#
## Test to ensure `update_author` doesn't raise any exceptions and completes
#def test_update_author_no_errors(client: TestClient, test_db: Session):
#    # Create a test author to update
#    author = Author(name="Original Name", is_active=True)
#    test_db.add(author)
#    test_db.commit()
#    test_db.refresh(author)
#
#    # Perform the update
#    response = client.put(
#        f"/{author.id}", json={"name": "Updated Name", "is_active": True}
#    )
#    assert response.status_code != 500  # Status code 500 indicates a server error
#
#
## Test to check if a non-existent author raises a 404 error
#def test_update_non_existent_author(client: TestClient):
#    non_existent_author_id = 99999
#    response = client.put(
#        f"/{non_existent_author_id}", json={"name": "Non-existent", "is_active": False}
#    )
#    assert response.status_code == 404
#
#
## Test to ensure `update_author` actually updates an author in the database
#def test_update_author_success(client: TestClient, test_db: Session):
#    # Create a test author to update
#    author = Author(name="Original Name", is_active=True)
#    test_db.add(author)
#    test_db.commit()
#    test_db.refresh(author)
#
#    # Perform the update
#    updated_data = {"name": "Updated Name", "is_active": False}
#    response = client.put(f"/{author.id}", json=updated_data)
#    assert response.status_code == 200
#
#    # Fetch the updated author from the database
#    updated_author = test_db.query(Author).filter(Author.id == author.id).first()
#    assert updated_author.name == updated_data["name"]
#    assert updated_author.is_active == updated_data["is_active"]
#
#
## Cleanup any overrides to return to normal operation
#def test_cleanup(override_get_db):
#    app.dependency_overrides = {}
#