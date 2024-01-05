import pytest

from app.crud.base import *
from sqlalchemy.orm import sessionmaker


from sqlalchemy import Column, Integer, create_engine
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from bson.objectid import ObjectId

DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1704487699809"

Base = declarative_base()


class SampleModel(Base):
    __tablename__ = "sample_model"
    id = Column(Integer, primary_key=True, index=True)


@pytest.fixture(scope="module")
def test_db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


# Make sure to install pymongo if you haven't already.
# You can install it using the command: pip install pymongo


@pytest.fixture(scope="module")
def test_db_session():
    # Your MongoDB connection string
    mongo_uri = 'mongodb://root:example@localhost:27017/code_robotics_1704487699809'
    
    # Connect to the MongoDB client
    client = MongoClient(mongo_uri)
    
    # Select the database
    db = client['code_robotics_1704487699809']  # Use the same db name as in the connection string
    
    # Before tests: (Optional) You can add setup code here if needed.
    
    yield db

    # After tests: (Optional) You could add teardown code here, like dropping the test database if needed.
    # For example, you could uncomment the following line to drop the test database after tests are done:
    # client.drop_database('code_robotics_1704487699809')

    # Close the connection to MongoDB
    client.close()


@pytest.fixture(scope="module")
def crud_base(test_db_session):
    return CRUDBase(model=SampleModel)


# Assuming 'crud_base' has a 'remove' method that accepts 'db' and 'id' parameters,
# and removes the document with that 'id' from the 'SampleModel' collection.

# Not changing the method name as per your requirement.
def test_remove_returns_correct_type(crud_base, test_db_session):
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    db = client.get_default_database()  # default database, or the specific db name if needed

    # Clear the 'SampleModel' collection
    db.SampleModel.delete_many({})

    # Insert a sample document
    sample = {"name": "Test Sample"}
    sample_id = db.SampleModel.insert_one(sample).inserted_id

    # Remove the sample document using crud_base.remove and capture the result
    removed_obj = crud_base.remove(db=db, id=sample_id)

    # Assert that the removed object is a dictionary (a document representation in PyMongo)
    assert isinstance(removed_obj, dict)

    # Clean up (optional if each test is designed to be completely independent)
    db.SampleModel.delete_many({})
    client.close()


# Assuming 'crud_base' will be adapted accordingly to work with MongoDB
# and 'SampleModel' is analogous to a MongoDB collection.

def test_remove_does_not_raise_error(crud_base, mongo_db):
    # Clear the collection
    mongo_db.SampleModel.delete_many({})

    # Insert sample document
    inserted_id = mongo_db.SampleModel.insert_one({}).inserted_id

    # Verify the removal does not raise an error and returns a non-None result
    assert crud_base.remove(db=mongo_db, id=inserted_id) is not None

# Fixture to create a Mongo database session
@pytest.fixture(scope="function")
def mongo_db():
    client = MongoClient('mongodb://root:example@localhost:27017/code_robotics_1704487699809')
    db = client.get_default_database()
    yield db
    # Cleanup code if necessary
    client.close()
