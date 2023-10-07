

from typing import Generator
from app.db.base_class import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app.crud import CRUDBase
from sqlalchemy.orm import scoped_session, sessionmaker
from app.crud.base import *

from sqlalchemy import Column, Integer, String, create_engine
import pytest

DATABASE_URL = "postgresql://username:password@localhost:5432/BooksDB"
engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(session_maker(bind=engine))


class SampleModel(Base):
    __tablename__ = "samples"
    id = Column(Integer, primary_key=True, autoincrement=True)


@pytest.fixture
def test_session() -> Generator:
    """Generate a test session for integration tests."""
    test_engine = create_engine(
        "postgresql://username:password@localhost:5432/BooksDB_test"
    )
    test_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    )
    yield test_session
    test_session.close()


@pytest.fixture(scope="module")
def crud_base() -> CRUDBase:
    return CRUDBase(SampleModel)


def test_remove(crud_base: CRUDBase, test_session: Session):
    sample_model = SampleModel()
    test_session.add(sample_model)
    test_session.commit()
    assert test_session.query(SampleModel).count() == 1

    removed_model = crud_base.remove(test_session, id=sample_model.id)

    assert removed_model is not None
    assert removed_model.id == sample_model.id
    assert test_session.query(SampleModel).count() == 0


def test_remove_invalid_id(crud_base: CRUDBase, test_session: Session):
    with pytest.raises(Exception):
        crud_base.remove(test_session, id=999)
