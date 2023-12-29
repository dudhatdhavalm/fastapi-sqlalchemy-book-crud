#from fastapi.testclient import TestClient
#from sqlalchemy.orm import sessionmaker
#from app.schemas.author import AuthorCreate
#
#from app.main import app
#
#
#import pytest
#from sqlalchemy import create_engine
#import pytest
#
#from app.api.endpoints.author import *
#from app.main import app
#from app.models.author import Author
#
## Set up a TestClient for the FastAPI application
#client = TestClient(app)
#
## Set up the test database and session
#DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
## Fixture for creating a DB session for the tests
#@pytest.fixture(scope="function")
#def db_session():
#    connection = engine.connect()
#    transaction = connection.begin()
#    session = TestingSessionLocal(bind=connection)
#    try:
#        yield session
#        session.commit()
#    except:
#        session.rollback()
#        raise
#    finally:
#        transaction.rollback()
#        connection.close()
#
#
## Test to check if get_author does not raise an error and returns a result
#def test_get_author_does_not_raise(db_session):
#    response = client.get("/authors")
#    assert response.status_code == 200
#    assert response.json() is not None
#
#
## Test to check if get_author retrieves data when there is an author
#def test_get_author_with_author(db_session):
#    author_data = {
#        "name": "John Doe",
#        "bio": "Bio of John Doe",
#    }
#    author = Author(**author_data)
#    db_session.add(author)
#    db_session.commit()
#
#    response = client.get("/authors")
#    assert response.status_code == 200
#    assert any(a["name"] == author_data["name"] for a in response.json())
#
#
## Test to check if get_author returns an empty list when there are no authors
#def test_get_author_empty(db_session):
#    authors = db_session.query(Author).all()
#    for author in authors:
#        db_session.delete(author)
#    db_session.commit()
#
#    response = client.get("/authors")
#    assert response.status_code == 200
#    assert response.json() == []
#