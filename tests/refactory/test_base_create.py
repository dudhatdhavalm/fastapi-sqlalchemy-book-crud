from app.db.base_class import Base
from sqlalchemy import create_engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, sessionmaker
from app.crud.base import *
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union


import pytest

import pytest
from sqlalchemy.orm import Session


from typing import Any, Dict, Generator, Generic, List, Optional, Type, TypeVar, Union
from app.crud.base import CRUDBase

from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def create(
        self, db: Session, *, obj_in: CreateSchemaType, created_by: Optional[str] = None
    ) -> ModelType:
        """
        Create a new database record.
        Also commits and refreshes the new database change.

        Args:
            db (Session): The database session.
            obj_in (CreateSchemaType): Object to be inserted.
            created_by (Optional[str], optional): The creator of the record. Defaults to None.
        Returns:
            ModelType: Returns the created database record.
        """
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["created_by"] = created_by
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def __init__(self, model: Type[ModelType]) -> None:
        """
        Class CRUDBase Constructor.

        Args:
            model (Type[ModelType]): The model based on which CRUD operations are made.
        """
        self.model = model

# Initialize test data
test_data = {"field1": "value1", "field2": "value2"}


@pytest.fixture(scope="module")
def test_db() -> Generator:
    # Set up a new database for testing
    engine = create_engine("postgresql://localhost/BooksDB")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a db session for test scopes
    session = TestingSessionLocal()

    yield session  # this is where the testing happens

    # Clean-up code (rollback transaction and close session)
    session.rollback()
    session.close()


def test_create(test_db: Session):
    # Create an object of class CRUDBase
    test_crud = CRUDBase(Base)

    # Create a new data row using the 'create' method
    new_base = test_crud.create(db=test_db, obj_in=test_data, created_by="test_user")

    assert isinstance(new_base, Base)
    assert new_base.field1 == test_data["field1"]
    assert new_base.field2 == test_data["field2"]
    assert new_base.created_by == "test_user"
