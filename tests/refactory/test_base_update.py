from sqlalchemy import create_engine
from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session, sessionmaker
from app.db.base_class import Base
from pydantic import BaseModel
from app.crud.base import *


from typing import Generic, Type, TypeVar

import pytest

# Prepare required imports for the test
ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class TestCRUDBase:
    @pytest.fixture
    def db(self):
        DB_URL = "postgresql://postgres:root@localhost:5432/BooksDB"
        engine = create_engine(DB_URL)
        session = sessionmaker(bind=engine)()
        yield session
        session.close()

    def test_update_no_errors(self, db: Session):
        class SampleModel(Base):
            id: int
            name: str

        class SampleSchema(BaseModel):
            name: str

        curd = CRUDBase(SampleModel)
        sample_instance = SampleModel(id=1, name="Initial")
        updated_sample_schema = SampleSchema(name="Updated")

        result = curd.update(db, db_obj=sample_instance, obj_in=updated_sample_schema)

        assert result is not None

    def test_update_obj_in_dict(self, db: Session):
        class SampleModel(Base):
            id: int
            name: str

        curd = CRUDBase(SampleModel)
        sample_instance = SampleModel(id=1, name="Initial")
        updated_sample_dict = {"name": "Updated"}

        result = curd.update(db, db_obj=sample_instance, obj_in=updated_sample_dict)

        assert result is not None
