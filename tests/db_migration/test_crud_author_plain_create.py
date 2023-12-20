#from sqlalchemy import create_engine
#from app.models.author import Author
#from app.schemas.author import AuthorCreate
#from app.crud.crud_author_plain import *
#
#
#from datetime import date
#from datetime import date
#
#import pytest
#from sqlalchemy.orm import Session, sessionmaker
#
#from app.crud.crud_author import CRUDAuthor
#
#
#@pytest.fixture(scope="module")
#def dummy_data() -> dict:
#    return {
#        "first_name": "John",
#        "last_name": "Doe",
#        "birthdate": date(1980, 1, 1),
#        "bio": "Some interesting bio",
#    }
#
#
#@pytest.fixture(scope="module")
#def obj_in(dummy_data: dict) -> AuthorCreate:
#    return AuthorCreate(**dummy_data)
#
#
#@pytest.fixture(scope="module")
#def crud_author() -> CRUDAuthor:
#    return CRUDAuthor(Author)
#
#
#def test_create(crud_author: CRUDAuthor, obj_in: AuthorCreate):
#    TEST_DB_URL = "postgresql://postgres:root@host.docker.internal:5432/"
#    engine = create_engine(TEST_DB_URL)
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    db: Session = SessionLocal()
#    result = crud_author.create(db, obj_in=obj_in)
#    assert result is not None
#