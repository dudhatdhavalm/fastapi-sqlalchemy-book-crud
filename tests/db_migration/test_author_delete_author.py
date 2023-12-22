#from fastapi.testclient import TestClient
#from app.schemas.author import AuthorCreate
#from sqlalchemy import create_engine
#
#from app.api.endpoints.author import *
#from sqlalchemy.orm import sessionmaker
#from app.main import app
#from app.api import dependencies
#from app.database import Base
#import pytest
#
#
#from app import crud
#
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703260584907"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
## Override get_db dependency to use the testing database
#@pytest.fixture(scope="function")
#def db_session():
#    connection = engine.connect()
#    transaction = connection.begin()
#    session = TestingSessionLocal(bind=connection)
#    yield session
#    session.close()
#    transaction.rollback()
#    connection.close()
#
#
#@pytest.fixture(scope="function")
#def client(db_session):
#    # Dependency override for the test client
#    def override_get_db():
#        try:
#            yield db_session
#        finally:
#            db_session.close()
#
#    app.dependency_overrides[dependencies.get_db] = override_get_db
#    return TestClient(app)
#
#
## Test to ensure the delete_author function does not throw errors when it's executed
#def test_delete_author_no_errors(client, db_session):
#    # Setup: create a test author
#    test_author = crud.author.create(
#        db_session, obj_in=AuthorCreate(name="Test Author", bio="Test Bio")
#    )
#    db_session.commit()
#    test_author_id = test_author.id
#    # Test
#    response = client.delete(f"/authors/{test_author_id}")
#    assert response.status_code == 200
#    assert response.json() == {
#        "detail": f"Author id {test_author_id} deleted successfully"
#    }
#
#
## Test to ensure that an author is actually deleted by delete_author
#def test_delete_author_success(client, db_session):
#    # Setup: create a test author
#    test_author = crud.author.create(
#        db_session, obj_in=AuthorCreate(name="Test Author", bio="Test Bio")
#    )
#    db_session.commit()
#    test_author_id = test_author.id
#    # Test
#    client.delete(f"/authors/{test_author_id}")
#    deleted_author = crud.author.get(db_session, id=test_author_id)
#    assert deleted_author is None
#
#
## Test to ensure that deleting a non-existent author raises a 404 error
#def test_delete_author_non_existent(client):
#    non_existent_author_id = 999999
#    response = client.delete(f"/authors/{non_existent_author_id}")
#    assert response.status_code == 404
#    assert "not found" in response.json().get("detail", "").lower()
#