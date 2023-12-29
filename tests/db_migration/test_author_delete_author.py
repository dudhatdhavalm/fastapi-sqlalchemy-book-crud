#from fastapi.testclient import TestClient
#from sqlalchemy.orm import sessionmaker
#
#
#import pytest
#from sqlalchemy import create_engine
#import pytest
#
#from app.api.dependencies import get_db
#from app.api.endpoints.author import *
#from app.main import app  # Assuming this is where the FastAPI app instance is located
#from app.models.author import (  # Assuming this is the correct path for the Author model
#    Author,
#)
#
## Set up the database URL
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#@pytest.fixture()
#def db_session():
#    connection = engine.connect()
#    transaction = connection.begin()
#    db = TestingSessionLocal(bind=connection)
#    try:
#        yield db
#    finally:
#        db.rollback()
#        connection.close()
#
#
#@pytest.fixture()
#def client(db_session):
#    def override_get_db():
#        try:
#            yield db_session
#        finally:
#            pass  # The db_session fixture will handle closing and rollback
#
#    # Dependency override for the database
#    app.dependency_overrides[get_db] = override_get_db
#
#    with TestClient(app) as client:
#        yield client
#
#
#def test_delete_author_without_errors(client, db_session):
#    author = Author(name="Test Author")
#    db_session.add(author)
#    db_session.commit()
#    author_id = author.id
#
#    response = client.delete(f"/authors/{author_id}")
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
#def test_delete_nonexistent_author(client):
#    response = client.delete("/authors/999999")
#    assert response.status_code == 404
#
#
#def test_delete_author_check_author_removed(client, db_session):
#    author = Author(name="Test Author")
#    db_session.add(author)
#    db_session.commit()
#    author_id = author.id
#
#    response = client.delete(f"/authors/{author_id}")
#    assert response.status_code == 200
#
#    deleted_author = db_session.query(Author).filter(Author.id == author_id).first()
#    assert deleted_author is None
#