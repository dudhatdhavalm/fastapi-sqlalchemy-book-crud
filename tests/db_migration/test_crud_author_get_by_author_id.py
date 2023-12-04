#from fastapi.encoders import jsonable_encoder
#from sqlalchemy import create_engine
#from app.schemas.author import AuthorCreate
#from app.models.author import Author
#from sqlalchemy.orm import Session, sessionmaker
#from app.crud.crud_author import CRUDAuthor
#import pytest
#from app.crud.crud_author import *
#
#DATABASE_URL = "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#
#engine = create_engine(DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#def create_test_author(db: Session, author_create: AuthorCreate) -> int:
#    db_author = Author(**jsonable_encoder(author_create.dict()))
#    db.add(db_author)
#    db.commit()
#    db.refresh(db_author)
#    return db_author.id
#
#
#@pytest.fixture(scope="module")
#def test_db():
#    return SessionLocal()
#
#
#@pytest.fixture(scope="module")
#def test_author(test_db: Session) -> int:
#    return create_test_author(test_db, AuthorCreate(name="Test", email="test@test.com"))
#
#
#def test_get_by_author_id(test_db: Session, test_author: int):
#    # We get instance of author by ID
#    result = CRUDAuthor().get_by_author_id(test_db, test_author)
#    assert (
#        result is not None
#    )  # The function should not throw any error and must return something.
#    assert isinstance(result, Author)
#    assert result.name == "Test"
#    assert result.email == "test@test.com"
#