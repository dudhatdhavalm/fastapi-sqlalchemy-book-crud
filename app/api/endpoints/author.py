from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
from pymongo import MongoClient
from app.schemas.author import AuthorCreate
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.schemas.author import AuthorUpdate, AuthorInDB
from app.crud.author_plain import update as update_author_plain, get_by_author_id

# Assuming we have a MongoDB connection string in DATABASE_URL
client = MongoClient(DATABASE_URL)
db = client.get_default_database()  # Replace with your database name if necessary 
authors_collection = db['authors']  # Replace with your collection name if necessary


@router.delete("/{author_id}", status_code=200)
def delete_author(*, author_id: int, db_client: MongoClient = Depends(dependencies.get_db_client)) -> dict:
    """
    Delete Author from MongoDB
    """
    authors_collection = db_client["mydatabase"]["authors"]  # Replace 'mydatabase' with your actual database name
    result = authors_collection.delete_one({"_id": ObjectId(str(author_id))})
    
    if result.deleted_count:
        return {"detail": f"Author id {author_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")

engine = create_engine(DATABASE_URL)


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db_client: MongoClient = Depends(dependencies.get_db_client)):
    # Assuming 'authors' is the collection where authors are stored
    author_collection = db_client["database_name"]["authors"] # Replace 'database_name' with actual database name
    author = author_collection.find_one({"_id": author_id})

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: str,
    author_in: AuthorUpdate,
    db_client: MongoClient = Depends(dependencies.get_db_client),
):
    db_collection = db_client.get_database()["authors"]
    
    existing_author = get_by_author_id(db_client, author_id)
    if existing_author is None:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")

    # Convert author_in, which is a Pydantic model, to a dictionary, excluding unset values 
    update_data = author_in.dict(exclude_unset=True)
    # Assuming that the update_data does not have '_id'
    
    # MongoDB expects the '_id' field to be an ObjectId, not a string, so we convert it
    author_id = ObjectId(author_id)
    
    result = db_collection.update_one(
        {"_id": author_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    
    # Retrieve the updated author from the database
    updated_author = db_collection.find_one({"_id": author_id})
    # Convert the MongoDB document to a Pydantic model
    return AuthorInDB(**updated_author)


@router.get("", status_code=200)
def get_author(*, db_client: MongoClient = Depends(dependencies.get_db_client)):
    author_collection = db_client.get_database().authors  # Assuming the database method gets the correct database and 'authors' is the collection
    authors = list(author_collection.find({}))  # Convert the cursor to a list
    return authors


# Assuming that DATABASE_URL is a MongoDB connection string

def recreate_database():
    # Create a MongoClient object to connect to the MongoDB server
    client = MongoClient(DATABASE_URL)

    # Specify the database name (you'll need to get this from your settings)
    db_name = "your_database_name"  # Modify with the actual database name
    db = client[db_name]

    # Define the collections to be created (or ensured)
    collections_to_ensure = [
        "authors",  # Add other collection names that you need to ensure exist
    ]

    # For each collection, you can ensure it is created and create indexes if necessary
    for collection_name in collections_to_ensure:
        collection = db[collection_name]

        # If there are any indexes you need to create for the collection, add them here
        # Example: collection.create_index([("field_name", pymongo.ASCENDING)])

        # The above code will create the collections if they do not already exist when
        # the first document is inserted into them. Collections and databases in MongoDB
        # are created when the first document is inserted.


recreate_database()

router = APIRouter()


@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, db_client: MongoClient = Depends(dependencies.get_db_client)
):
    # Convert author_in, which is a Pydantic model, to a dictionary
    author_dict = author_in.dict()
    # Insert the author into MongoDB and retrieve the inserted_id
    created_author = authors_collection.insert_one(author_dict)
    # Add the inserted_id to the author_dict
    author_dict['_id'] = created_author.inserted_id
    return author_dict
