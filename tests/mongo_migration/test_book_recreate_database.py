from app.models.book import Base
from sqlalchemy import create_engine
from app.settings import DATABASE_URL
from app.api.endpoints.book import *
from sqlalchemy.orm import Session, sessionmaker
import pytest


import pytest
from sqlalchemy.orm import Session
from pymongo import MongoClient
from app.api.endpoints import book

# Connection string to your MongoDB instance
mongodb_uri = 'mongodb://localhost:27017/test_database'

engine = create_engine(DATABASE_URL)


def test_recreate_database(db_session):
    client = MongoClient('localhost', 27017)
    db = client['test_database']  # Define your database
    collections = db.collection_names(include_system_collections=False)
    
    # Ensure collections exist
    assert collections != []
    
    # Drop all collections to recreate the database
    for collection in collections:
        db[collection].drop()
        
    collections = db.collection_names(include_system_collections=False)
    
    # Ensure collections do not exist
    assert collections == []


@pytest.fixture(scope="function")
def db_session():
    client = MongoClient(mongodb_uri)
    _db = client.get_default_database()
    
    yield _db
    
    client.drop_database(_db)
    client.close()
