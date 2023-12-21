from app.crud.base import *
from sqlalchemy import Column, Integer, create_engine
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import pytest






import pytest
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# Assuming that 'mongodb_uri' and 'dbname' are defined either as variables 
# or fetched from a config file/environment variables.
mongodb_uri = 'your_mongodb_uri'
dbname = 'your_test_database_name'

DATABASE_URL = "sqlite://"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModelTest = declarative_base()


@pytest.fixture(scope="function")
def db_session() -> Collection:
    client = MongoClient(mongodb_uri)
    database: Database = client[dbname]
    collection: Collection = database['test_collection']  # Replace with a test collection name

    # Since MongoDB is schema-less, we don't create or drop the database schema,
    # we simply clear the collection after each test.
    yield collection
    
    # After the test(s) are done, cleanup by dropping the test collection.
    collection.drop()

    # Close the client connection
    client.close()


@pytest.fixture
def mock_model(db_session: Session):
    class MockModel(BaseModelTest):
        __tablename__ = "test_table"
        id = Column(Integer, primary_key=True)

    BaseModelTest.metadata.create_all(bind=engine)
    return MockModel


def test_CRUDBase_init_no_errors(mock_model):
    assert (
        CRUDBase(mock_model) is not None
    ), "CRUDBase __init__ raised an error with valid model"
