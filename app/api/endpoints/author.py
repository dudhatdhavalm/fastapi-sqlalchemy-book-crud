from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorCreate
from pymongo.database import Database
from bson import ObjectId
from app.schemas.author import AuthorUpdate

router = APIRouter()  # Make sure to define the APIRouter if it's not already defined in the actual context.

# Assuming DATABASE_URL of MongoDB follows the pattern: 'mongodb://user:pass@host:port/database_name'

client = MongoClient(DATABASE_URL)
db = client.get_default_database()


@router.delete("/{author_id}", status_code=200)
def delete_author(*, author_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author using PyMongo
    """
    deleted_result = db.authors.delete_one({"_id": ObjectId(author_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    return {"detail": f"Author id {author_id} deleted successfully"}

# Assumes settings.DATABASE_URL is a MongoDB connection URI
client = MongoClient(DATABASE_URL)


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db: Database = Depends(dependencies.get_db)):
    author = db.authors.find_one({"_id": author_id})
    
    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    
    return author


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: str,  # Changed to str because MongoDB IDs are usually strings.
    author_in: AuthorUpdate,  # Assuming AuthorUpdate is a Pydantic model.
    db: Database = Depends(dependencies.get_db),  # Change the type hint to pymongo's Database.
):
    author_collection = db.get_collection("authors")  # Assuming the collection name is authors.
    
    # Attempt to convert author_id to ObjectId, if necessary.
    try:
        oid = ObjectId(author_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid author ID format") from e

    # Find the existing author document by ID.
    existing_author = author_collection.find_one({"_id": oid})
    
    if existing_author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    # Update the author document.
    # We need to convert the Pydantic model into a dictionary, excluding unset fields,
    # and then exclude ID if it is present.
    update_data = author_in.dict(exclude_unset=True, exclude_none=True)
    update_data.pop('id', None)  # Exclude ID from update data if present.

    update_result = author_collection.update_one(
        {"_id": oid},
        {"$set": update_data}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not updated")

    # Return the updated author document or just the ID; depending on actual requirements.
    updated_author = author_collection.find_one({"_id": oid})
    if not updated_author:
        raise HTTPException(status_code=404, detail="Updated author not found after update operation")

    return updated_author


# Assuming dependencies.get_db returns a PyMongo database connection
@router.get("", status_code=200)
def get_author(*, db: Database = Depends(dependencies.get_db)):
    # Assuming 'authors' is the collection where authors' data is stored
    author_collection = db['authors']
    
    # Retrieve the first document found in the 'authors' collection
    # You might need to adjust this based on how you would like to retrieve the author(s) information
    author = author_collection.find_one()

    # You might want to convert the _id field from ObjectId to string if you want to send it as JSON
    if author and "_id" in author:
        author["_id"] = str(author["_id"])
    
    # Returning the author document or None if not found
    return author
db = client.my_database  # Replace with your actual database name

engine = create_engine(DATABASE_URL)


def recreate_database():
    # In MongoDB, you don't typically create collections
    # as they are created automatically when you insert documents.
    # However, you may want to create indices or set collection options here if needed.
    # For example:
    # db.authors.create_index([('author_id', pymongo.ASCENDING)], unique=True)
    pass  # Remove this line if you add any actual functionality


@router.post("", status_code=200)
def create_author(
    *, author_in: dict, db = Depends(dependencies.get_db)
):
    authors_collection = db['authors']
    result = authors_collection.insert_one(author_in.dict())
    new_author = authors_collection.find_one({"_id": result.inserted_id})
    return new_author


recreate_database()

router = APIRouter()
