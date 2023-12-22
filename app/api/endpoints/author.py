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
from fastapi import Depends, HTTPException, APIRouter
from app.schemas.author import AuthorUpdate

router = APIRouter()  # Assuming that router is earlier defined somewhere in your code

engine = create_engine(DATABASE_URL)


# Assuming DATABASE_URL is the MongoDB connection string

def recreate_database():
    client = MongoClient(DATABASE_URL)
    
    # Retrieve the database name from DATABASE_URL, you might need to adjust parsing according to your URL format
    db_name = DATABASE_URL.split('/')[-1]
    db = client[db_name]
    
    # Drop each collection in the database
    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)


@router.get("", status_code=200)
def get_author(*, db: Database = Depends(dependencies.get_db)):
    author_collection = db.get_collection("author")
    author = author_collection.find_one()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}",status_code=200)
def delete_author(*, author_id: int, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author
    """
    # Using PyMongo's delete_one() method to delete the author by its "_id"
    result = db.authors.delete_one({"_id": author_id})
    if result.deleted_count:
        return {"detail": f"Author id {author_id} deleted successfully"}
    else:
        # After trying to delete, if no document is found, it likely means the author wasn't found
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: int,
    author_in: AuthorUpdate,
    db: Database = Depends(dependencies.get_db),
):
    authors_collection = db.get_collection('authors')  # Assuming 'authors' is the collection name
    result = authors_collection.find_one({"_id": author_id})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    
    update_data = author_in.dict(exclude_unset=True)
    authors_collection.update_one({"_id": author_id}, {"$set": update_data})
   
    # Retrieve updated author data
    updated_author = authors_collection.find_one({"_id": author_id})
    return updated_author


# You would previously need to have the 'router' defined as an instance of APIRouter but since
# this declaration is not required in your question, it's not included here in the code snippet.

@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db: Database = Depends(dependencies.get_db)):
    # Assuming we use a collection called "authors" to store author data
    author = db.authors.find_one({"_id": author_id})

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


recreate_database()

router = APIRouter()


@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, db: Database = Depends(dependencies.get_db)
):
    # Convert the AuthorCreate Pydantic model to a dictionary
    author_data = author_in.dict()
    # Insert the author data into the MongoDB collection
    author_id = db.authors.insert_one(author_data).inserted_id
    # Retrieve the inserted author document using the new author ID
    author = db.authors.find_one({"_id": author_id})
    # Note: You might want to exclude or transform the '_id' field as needed
    # to ensure it's serializable in the response, e.g., str(author['_id'])
    return author
