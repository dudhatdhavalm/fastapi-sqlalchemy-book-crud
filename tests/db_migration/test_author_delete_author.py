#from app.api.endpoints.author import *
#from fastapi.testclient import TestClient
#from sqlalchemy import create_engine
#from fastapi import status
#from sqlalchemy.orm import Session, sessionmaker
#import pytest
#
## Update this values with your database connection info.
#db_settings = {
#    "user": "root",
#    "password": "postgres",
#    "host": "localhost",
#    "port": "5432",
#    "database": "test_db",
#}
#
#DATABASE_URL_TEST = f'postgresql://{db_settings["user"]}:{db_settings["password"]}@{db_settings["host"]}:{db_settings["port"]}/{db_settings["database"]}'
#
#engine = create_engine(DATABASE_URL_TEST)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#@pytest.fixture
#def test_db():
#    Base.metadata.create_all(bind=engine)
#    db = TestingSessionLocal()
#    yield db
#    db.close()
#    Base.metadata.drop_all(bind=engine)
#
#
#@pytest.fixture
#def test_client():
#    client = TestClient(app)
#    yield client
#
#
#def test_delete_author(test_db: Session, test_client: TestClient):
#    # Create a new author.
#    new_author = create_author(
#        author_in=AuthorCreate(name="John Doe", book="My Life", age=30), db=test_db
#    )
#    response = test_client.delete(f"/authors/{new_author.id}")
#    assert response.status_code == status.HTTP_200_OK
#    assert response.json() == {
#        "detail": f"Author id {new_author.id} deleted successfully"
#    }
#    # Check if the author was deleted.
#    deleted_author = get_by_id(author_id=new_author.id, db=test_db)
#    assert deleted_author is None
#