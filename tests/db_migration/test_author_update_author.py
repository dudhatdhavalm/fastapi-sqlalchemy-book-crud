#from app.api.endpoints.author import *
#from sqlalchemy import create_engine
#from fastapi import HTTPException
#from app.api import dependencies
#from app.crud import crud_author_plain
#from sqlalchemy.orm import Session, sessionmaker
#import pytest
#
#
#from typing import Generator
#from app.schemas.author import AuthorCreate, AuthorUpdate
#
## Define the database URL, which will be used to set up test session
#DATABASE_URL = "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#
#
## Fixture for SQL Alchemy session
#@pytest.fixture(scope="module")
#def db() -> Generator:
#    engine = create_engine(DATABASE_URL)
#    with Session(engine) as session:
#        yield session
#
#
## Test object creation before testing update operation
#@pytest.fixture(scope="module")
#def test_obj(db: Session):
#    test_create_obj = AuthorCreate(
#        name="Test Name", surname="Test Surname", photo="Test Photo"
#    )
#    return crud_author_plain.create(db, obj_in=test_create_obj)
#
#
#def test_update_author(db: Session, test_obj):
#    update_obj = AuthorUpdate(
#        name="New Test Name", surname="New Test Surname", photo="New Test Photo"
#    )
#    result = update_author(author_id=test_obj.id, author_in=update_obj, db=db)
#    assert result is not None
#
#
#def test_update_author_nonexistent_author(db: Session):
#    nonexistent_author_id = 99999
#    update_obj = AuthorUpdate(
#        name="New Test Name", surname="New Test Surname", photo="New Test Photo"
#    )
#    with pytest.raises(HTTPException):
#        update_author(nonexistent_author_id, author_in=update_obj, db=db)
#
#
#def test_update_author_with_invalid_data(db: Session, test_obj):
#    invalid_update_obj = AuthorUpdate(name="", surname="", photo="")
#    with pytest.raises(ValueError):
#        update_author(author_id=test_obj.id, author_in=invalid_update_obj, db=db)
#