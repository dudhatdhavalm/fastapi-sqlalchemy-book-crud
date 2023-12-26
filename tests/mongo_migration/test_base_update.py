from typing import Optional, Type

import pytest
from unittest.mock import MagicMock

from app.crud.base import *
from pydantic import BaseModel
from sqlalchemy.orm import Session
from unittest.mock import patch
from bson import ObjectId  # Used for generating ObjectId's for MongoDB documents




class MockModel(BaseModel):
    id: int
    name: str
    modified_by: Optional[int] = None


class MockUpdateSchema(BaseModel):
    name: Optional[str] = None
    modified_by: Optional[int] = None




@pytest.fixture(scope="function")
def mock_session() -> MagicMock:
    db_session = MagicMock(spec=Session)
    db_session.add = MagicMock()
    db_session.commit = MagicMock()
    db_session.refresh = MagicMock()
    return db_session


@pytest.fixture(scope="function")
def crud_base() -> CRUDBase:
    return CRUDBase(model=MockModel)



def test_update_no_errors(crud_base: CRUDBase):
    """
    Test if the update function executes without errors using PyMongo.
    """
    # In PyMongo, the 'id' field is typically an '_id' field, holding an ObjectId.
    # In an actual MongoDB document, '_id' is automatically generated. For testing,
    # we'll manually create an ObjectId since we are not really inserting the document
    # into MongoDB.
    db_obj = MockModel(_id=ObjectId(), name="initial")
    
    # Update data is assumed to be the same; it's just a dictionary update payload.
    update_data = {"name": "updated", "modified_by": 2}
    
    # Assuming the update method of a PyMongo-based CRUDBase would be similar,
    # but we would pass a PyMongo collection mock instead of a SQLAlchemy session.
    with patch('pymongo.collection.Collection') as mock_collection:
        returned_obj = crud_base.update(
            db=mock_collection, db_obj=db_obj, obj_in=update_data, modified_by=3
        )
    
    assert returned_obj is not None


