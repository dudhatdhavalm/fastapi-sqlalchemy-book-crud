#from sqlalchemy import create_engine
#import pytest
#
#from app.crud.crud_author_plain import *
#from app.models.author import Author
#from app.crud.crud_author_plain import CRUDAuthor
#
#from app.crud.crud_author_plain import CRUDAuthor
#
#
#import pytest
#from sqlalchemy.orm import Session, sessionmaker
#
## Replace with your actual database url
#DATABASE_URL = "postgresql://postgres:root@host.docker.internal:5432/"
#
#engine = create_engine(DATABASE_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
## Fixture to provide database session for each test
#@pytest.fixture(scope="module")
#def db() -> Session:
#    session = SessionLocal()
#    yield session
#    session.close()
#
#
#def test_get_authors(db):
#    author_crud = CRUDAuthor()
#    authors = author_crud.get(db)
#    assert authors is not None
#    assert isinstance(authors, list)
#
#
#def test_get_authors_pagination(db):
#    author_crud = CRUDAuthor()
#    authors_page_1 = author_crud.get(db, skip=0, limit=2)
#    authors_page_2 = author_crud.get(db, skip=2, limit=2)
#    assert authors_page_1 is not None
#    assert authors_page_2 is not None
#
#
#def test_get_authors_zero_limit(db):
#    author_crud = CRUDAuthor()
#    authors = author_crud.get(db, limit=0)
#    assert authors is not None
#    assert len(authors) == 0
#