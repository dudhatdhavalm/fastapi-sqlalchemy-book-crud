#from sqlalchemy import create_engine
#from typing import Generator
#
#from app.crud.crud_author_plain import *
#from app.models.author import Author
#from app.crud.crud_author_plain import CRUDAuthor
#
#import pytest
#from sqlalchemy.orm import Session, sessionmaker
#
## Connection string for a test database
#DATABASE_URL = "postgresql://postgres:root@host.docker.internal:5432/testdb"
#
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
## Fixture for database connection
#@pytest.fixture(scope="module")
#def db() -> Generator:
#    conn = engine.connect()
#    txn = conn.begin()
#
#    yield Session(bind=conn)
#
#    Session.close_all()
#    txn.rollback()
#    conn.close()
#
#
## The database needs to be properly set up before these tests can be executed.
## Test that it does.
#@pytest.fixture(scope="module", autouse=True)
#def check_database(db: Session):
#    assert engine.dialect.has_table(
#        engine, "author"
#    ), "Test database is not properly set up. 'author' table does not exist."
#
#
## Test case - get_by_author_id - nominal case
#def test_get_by_author_id(db: Session):
#    crud_author = CRUDAuthor()
#    author = crud_author.get_by_author_id(db, 1)
#    assert author is not None
#
#
## Test case - get_by_author_id - invalid case
#def test_get_by_author_id_invalid(db: Session):
#    crud_author = CRUDAuthor()
#    author = crud_author.get_by_author_id(db, 99999999)
#    assert author is None
#