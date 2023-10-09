from datetime import date
from app.crud.crud_author_plain import *
from app.crud.crud_author import CRUDAuthor
from app.models.author import Author


from datetime import date

import pytest
from sqlalchemy.orm import Session
from app.schemas.author import AuthorCreate
from pymongo import MongoClient
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from pymongo.errors import OperationFailure


def test_create_author(setup_db, author_data):
    author_crud = CRUDAuthor()

    author_id = author_crud.create(db=setup_db, obj_in=author_data)

    author = setup_db.find_one({'_id': ObjectId(author_id)})

    assert author is not None
    assert author['name'] == "John Doe"
    assert author['birth_date'] == date(1960, 1, 1)
    
    # Test with invalid birth_date
    invalid_author_data = AuthorCreate(
        name="Invalid Author", birth_date=date(1820, 1, 1)
    )

    with pytest.raises(OperationFailure):
        author_crud.create(db=setup_db, obj_in=invalid_author_data)


@pytest.fixture
def setup_db():
    client = MongoClient('localhost', 27017)
    db = client['test_db']
    yield db
    client.drop_database('test_db')
    client.close()


def author_data():
    return {'name': "John Doe", 'birth_date': datetime(1960, 1, 1)}
