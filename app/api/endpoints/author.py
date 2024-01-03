from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
from pymongo import MongoClient
from app.models.author import AuthorModel  # Assuming this is the name of your MongoDB model/doc
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorCreate
from pymongo.database import Database
from fastapi import HTTPException, Depends, APIRouter
from app.schemas.author import AuthorUpdate
from bson import ObjectId

# Assuming router has been defined earlier as APIRouter
router = APIRouter()


router = APIRouter()  # Assuming the router should be defined somewhere in your actual code.


@router.delete("/{author_id}", status_code=200)
def delete_author(*, author_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author
    """
    deleted_count = db.authors.delete_one({'_id': ObjectId(author_id)}).deleted_count
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    return {"detail": f"Author id {author_id} deleted successfully"}


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: int,
    author_in: AuthorUpdate,
    db: Database = Depends(dependencies.get_db),
):
    authors_collection = db.get_collection("authors")
    result = authors_collection.find_one({"_id": author_id})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    updated_document = {"$set": author_in.dict(exclude_unset=True)}
    authors_collection.update_one({"_id": author_id}, updated_document)
    
    author = authors_collection.find_one({"_id": author_id})
    return author


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db: Database = Depends(dependencies.get_db)):
    author_collection = db.get_collection('authors')  # Assume 'authors' is the collection name
    author = author_collection.find_one({'_id': author_id})
    
    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


# Modified get_authors function using PyMongo
@router.get("", status_code=200)
def get_author(*, db: Database = Depends(dependencies.get_db)):
    # Assuming 'authors' is the name of the collection where authors are stored
    authors_collection = db['authors']
    # MongoDB find command to get all authors
    authors_cursor = authors_collection.find({})
    # Convert cursor to list of dicts (assuming the data can fit into memory)
    authors = list(authors_cursor)
    return authors

# MongoDB connection string
connection_string = DATABASE_URL  

engine = create_engine(DATABASE_URL)


def recreate_database():
    client = MongoClient(connection_string)
    db_name = client.get_default_database()  # Assuming the DB name is in the connection string

    # List of collections names that should exist
    collections_to_create = ['authors', 'other_collection']  # Add other collection names as required

    existing_collections = db_name.list_collection_names()
    for collection in collections_to_create:
        if collection not in existing_collections:
            db_name.create_collection(collection)
    
    # You might want to create indexes or perform other setup tasks here as well

    client.close()  # Closing the connection; Remove if using connection pooling or context management



@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, db: Database = Depends(dependencies.get_db)
):
    author_dict = author_in.dict()  # Converting Pydantic model to dictionary
    author_collection = db.get_collection("authors")  # Accessing the 'authors' collection
    inserted_result = author_collection.insert_one(author_dict)
    
    # Fetching the newly created document using the inserted_id
    created_author = author_collection.find_one({"_id": inserted_result.inserted_id})
    
    return created_author


recreate_database()

router = APIRouter()
