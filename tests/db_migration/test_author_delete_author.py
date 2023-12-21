#from fastapi.testclient import TestClient
#from sqlalchemy import create_engine
#
#from app.api.endpoints.author import *
#
#from app.api.endpoints.author import router
#from app.api.endpoints.author import router
#from sqlalchemy.orm import sessionmaker
#
#
#import pytest
#import pytest
#from app.models.author import (  # Assuming Author model is also in app.models.author
#    Author,
#    Base,
#)
#
## Setup the database and the client
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703158870842"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#client = TestClient(router)
#
#
#@pytest.fixture(scope="function")
#def db_session():
#    Base.metadata.create_all(bind=engine)
#    db_session = TestingSessionLocal()
#    try:
#        # Add mock author to the database
#        mock_author = Author(name="Test Author")
#        db_session.add(mock_author)
#        db_session.commit()
#        db_session.refresh(mock_author)
#
#        yield db_session, mock_author.id
#    finally:
#        db_session.rollback()
#        db_session.close()
#        Base.metadata.drop_all(bind=engine)
#
#
#def test_delete_author(db_session):
#    db, author_id = db_session
#    response = client.delete(f"/{author_id}", headers={"db": db})
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
#def test_delete_nonexistent_author(db_session):
#    db, _ = db_session
#    non_existent_id = 999999
#    response = client.delete(f"/{non_existent_id}", headers={"db": db})
#    assert response.status_code == 404
#
#
#def test_delete_author_invalid_id(db_session):
#    db, _ = db_session
#    invalid_id = "invalid_id"
#    response = client.delete(f"/{invalid_id}", headers={"db": db})
#    assert response.status_code == 422
#from app.models.author import (  # Assuming Author model is also in app.models.author
#    Author,
#    Base,
#)
#