from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorUpdate

client = MongoClient()  # Assuming a running mongodb instance on localhost
db = client['mydatabase']  # Use your database here
db = client.test


client = MongoClient(DATABASE_URL)
db = client.get_database()    # Assuming the database name is already defined in settings

# Initialize the client
client = MongoClient(DATABASE_URL)

mongo_client = MongoClient()


@router.delete("/{author_id}",status_code=200)
def delete_author(*, author_id: int) -> dict:
    """
    Delete Author
    """
    authors = db['authors']  # Use your collection here
    result = authors.delete_one({"_id": ObjectId(author_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"detail": f"Author id {author_id} deleted successfully"}
db = mongo_client['test']

engine = create_engine(DATABASE_URL)



@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: int,
    author_in: AuthorUpdate,
    db = Depends(dependencies.get_db),
):
    authors_collection = db["authors"]

    result = authors_collection.find_one({"_id": author_id})

    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    result = authors_collection.update_one({"_id": author_id}, {"$set": author_in.dict()})

    return result.modified_count


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db = client['your_database_name']


recreate_database()


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: str):

    author = db.authors.find_one({"_id": ObjectId(author_id)})

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


@router.get("", status_code=200)
def get_author(*, db: Depends(dependencies.get_db)):
    # Specify the database
    db = client['database_name']
  
    # Specify the collection
    authors = db['collection_name']
  
    # Retrieve the author
    author = authors.find_one({})
    return author

router = APIRouter()


@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, 
):
    author = db.author_plain.insert_one(author_in.dict())
    if author.acknowledged:
        return {"_id": str(author.inserted_id)}
    else:
        raise HTTPException(status_code=400, detail="Author could not be created")
