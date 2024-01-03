#from sqlalchemy.orm import sessionmaker
#
#from app.api.dependencies import get_db
#from fastapi import FastAPI
#from fastapi.exceptions import HTTPException
#from sqlalchemy import create_engine
#import pytest
#from app.crud.author import author_plain
#from app.models.author import Author, Base
#
#
#import pytest
#
#from app.models.author import Author, Base
#from fastapi import HTTPException
#from app.api.endpoints.author import *
#
#
## Fixture to create a new database engine and session for testing
#@pytest.fixture(scope="module")
#def test_engine():
#    engine = create_engine(
#        "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704237404964"
#    )
#    Base.metadata.create_all(engine)
#    return engine
#
#
#@pytest.fixture(scope="module")
#def test_db_session(test_engine):
#    connection = test_engine.connect()
#    transaction = connection.begin()
#    session_local = sessionmaker(autocommit=False, autoflush=False, bind=connection)
#    session = session_local()
#    yield session  # Use the session in tests.
#    session.close()
#    transaction.rollback()
#    connection.close()
#    Base.metadata.drop_all(test_engine)
#
#
## Fixture to override the get_db dependency with the test database session
#@pytest.fixture
#def override_get_db(test_db_session):
#    def _get_db_override():
#        try:
#            yield test_db_session
#        finally:
#            test_db_session.close()
#
#    return _get_db_override
#
#
## Override the get_db dependency to use the overriden one
#app.dependency_overrides[get_db] = override_get_db
#
#
## Test to ensure get_by_id does not throw an error and returns a result with valid author_id
#def test_get_by_id_no_error(test_db_session, override_get_db):
#    # Setup - create a test author
#    test_author = Author(name="Test Author", bio="Bio of test author")
#    test_db_session.add(test_author)
#    test_db_session.commit()
#    test_db_session.refresh(test_author)
#
#    # Test
#    author_id = test_author.id
#    response = get_by_id(author_id=author_id, db=next(override_get_db()))
#    assert response is not None
#
#    # Cleanup
#    test_db_session.delete(test_author)
#    test_db_session.commit()
#
#
## Test to ensure get_by_id raises HTTPException with status code 404 for a non-existent author_id
#def test_get_by_id_non_existent_author(override_get_db):
#    non_existent_author_id = 0  # Assuming 0 is not a valid ID.
#    with pytest.raises(HTTPException) as exc:
#        get_by_id(author_id=non_existent_author_id, db=next(override_get_db()))
#    assert exc.value.status_code == 404
#    assert "not found" in exc.value.detail
#