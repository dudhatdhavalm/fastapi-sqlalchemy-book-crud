from sqlalchemy.orm import Session, sessionmaker

from app.crud.base import *
from sqlalchemy.ext.declarative import declarative_base

import pytest
from pydantic import BaseModel


import pytest
from sqlalchemy import Column, Integer, String, create_engine
from typing import Type

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703158870842"

Base = declarative_base()


class FakeModel(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    created_by = Column(String)


class FakeCreateSchema(BaseModel):
    created_by: str


@pytest.fixture(scope="module")
def db_session() -> Session:
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create(db_session: Session):
    crud = CRUDBase(model=FakeModel)
    schema = FakeCreateSchema(created_by="test_user")
    db_obj = crud.create(db_session, obj_in=schema)
    assert db_obj is not None


def test_create_adds_new_record(db_session: Session):
    crud = CRUDBase(model=FakeModel)
    initial_count = db_session.query(FakeModel).count()
    schema = FakeCreateSchema(created_by="test_user")
    _ = crud.create(db_session, obj_in=schema)
    assert db_session.query(FakeModel).count() == initial_count + 1
