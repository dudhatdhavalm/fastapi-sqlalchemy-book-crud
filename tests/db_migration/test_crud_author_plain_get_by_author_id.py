#from sqlalchemy import create_engine
#from app.models.author import Author
#from sqlalchemy.orm import Session, sessionmaker
#import pytest
#from app.crud.crud_author_plain import *
#
## Sample data for Testing
#SAMPLE_AUTHOR_DATA = {"id": 1, "name": "Test Author", "dob": date(1990, 1, 1)}
#
#
## Pytest Fixture for Setting Up the Database
#@pytest.fixture
#def test_db():
#    DB_URL = "postgresql://root:postgres@localhost/test_db"
#    engine = create_engine(DB_URL)
#    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#    # Create a session for testing
#    with TestingSessionLocal() as test_session:
#        yield test_session
#
#
## Test for checking the get_by_author_id function
#def test_get_by_author_id(test_db):
#    crud_author = CRUDAuthor()
#    # Add dummy author to the db
#    test_db.add(Author(**SAMPLE_AUTHOR_DATA))
#    test_db.commit()
#
#    author = crud_author.get_by_author_id(test_db, 1)
#    assert author is not None
#
#
## Test for checking the get_by_author_id function with nonexistent id
#def test_get_by_author_id_nonexistent(test_db):
#    crud_author = CRUDAuthor()
#    # Add dummy author to the db
#    test_db.add(Author(**SAMPLE_AUTHOR_DATA))
#    test_db.commit()
#
#    author = crud_author.get_by_author_id(test_db, 999)
#    assert author is None
#
#
## Test for checking get_by_author_id function when id is not an integer
#def test_get_by_author_id_noninteger(test_db):
#    crud_author = CRUDAuthor()
#    with pytest.raises(TypeError):
#        author = crud_author.get_by_author_id(test_db, "string")
#
#
## Test for checking get_by_author_id function when id is a negative number
#def test_get_by_author_id_negative(test_db):
#    crud_author = CRUDAuthor()
#    # Add dummy author to the db
#    test_db.add(Author(**SAMPLE_AUTHOR_DATA))
#    test_db.commit()
#
#    author = crud_author.get_by_author_id(test_db, -1)
#    assert author is None
#