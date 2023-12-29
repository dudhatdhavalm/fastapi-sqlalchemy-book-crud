# Define necessary imports
from typing import Type

import pytest
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from pydantic import BaseModel, create_model
from sqlalchemy import Column, Integer, String, create_engine

from app.crud.base import *


from typing import Type

# Define the format of the model for SQLAlchemy and Pydantic
Base = declarative_base()


class ExampleModel(Base):
    __tablename__ = "example"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    modified_by = Column(Integer)


ExampleSchema = create_model("ExampleSchema", name=(str, ...), modified_by=(int, ...))


# Define a PostgreSQL connection URI
DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def example_model(db: Session) -> ExampleModel:
    example_obj = ExampleModel(name="Old Name", modified_by=1)
    db.add(example_obj)
    db.commit()
    db.refresh(example_obj)
    return example_obj


@pytest.fixture(scope="function")
def crud_base() -> CRUDBase:
    return CRUDBase(model=ExampleModel)


class TestCRUDBase:
    def test_update_no_errors(
        self, db: Session, example_model: ExampleModel, crud_base: CRUDBase
    ):
        """
        Test if CRUDBase.update method executes without raising any errors
        with valid arguments.
        """
        update_obj = ExampleSchema(name="New Name", modified_by=2)
        try:
            result = crud_base.update(
                db, db_obj=example_model, obj_in=update_obj, modified_by=2
            )
            assert result is not None
        except Exception as e:
            pytest.fail(f"Update method raised an exception: {e}")
