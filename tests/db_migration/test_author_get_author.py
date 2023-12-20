#from app.api.endpoints.author import *
#from app.api.dependencies import get_db
#from app.schemas.author import AuthorCreate
#from app.crud import author as author_crud
#
#
#import pytest
#import pytest
#from sqlalchemy.orm import Session
#
#
#@pytest.fixture
#def test_get_author(create_author_fixture, db_session):
#    author = get_author(db=db_session)
#    assert author is not None
#
#
## Edge case:
## Test when no authors exist in the database
#def test_get_author_no_authors(db_session: Session):
#    author = get_author(db=db_session)
#    assert author is None
#