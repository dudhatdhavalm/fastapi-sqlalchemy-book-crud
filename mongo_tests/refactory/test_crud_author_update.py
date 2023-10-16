from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.crud.crud_author import *
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.author import CRUDAuthor

import pytest
from typing import Any, Dict, Union
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['test_database']

DATABASE_URL = "postgresql://postgres:root@localhost/BooksDB"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def update_author():
    return {"name": "Updated Test Author"}


def test_update(test_author, update_author):
    client = MongoClient('localhost', 27017)
    db = client['test_database']
    authors = db['authors']
    
    new_author = authors.update_one({"name": test_author}, {"$set": update_author})
    updated_author = authors.find_one({"name": update_author['name']})
   
    assert updated_author is not None
    assert updated_author['name'] == "Updated Test Author"

db: Session = SessionLocal()


def test_author():
    author = db.author.find_one({'id': 1})
    return author
