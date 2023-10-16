import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from app.crud.base import *


from typing import Generator


@pytest.fixture(scope="module")
def db() -> Generator:
    engine = create_engine("postgresql://postgres:root@localhost/BooksDB")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: Session = SessionLocal()
    yield session
    session.rollback()
    session.close()


def test_remove(db: Session) -> None:
    crud_base = CRUDBase(Base)
    obj = crud_base.remove(db, id=1)
    assert obj is not None


def test_remove_with_invalid_id(db: Session) -> None:
    crud_base = CRUDBase(Base)
    try:
        crud_base.remove(db, id=999999)
    except Exception as e:
        assert isinstance(e, Exception)


def test_remove_with_non_integer_id(db: Session) -> None:
    crud_base = CRUDBase(Base)
    try:
        crud_base.remove(db, id="non integer id")
    except Exception as e:
        assert isinstance(e, Exception)
