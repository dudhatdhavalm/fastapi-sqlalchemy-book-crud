from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.author import AuthorCreate, AuthorUpdate
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.api import dependencies
from app.settings import DATABASE_URL
from app.models.author import Base
from app import crud
from pymongo import MongoClient
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.author import AuthorCreate
from pymongo.collection import Collection
from app.schemas.author import AuthorUpdate

# Assuming you have MongoDB connection settings defined in DATABASE_URL or use a configuration dictionary

client = MongoClient(DATABASE_URL)


@router.get("", status_code=200)
def get_author(*, db: Collection = Depends(dependencies.get_db)):
    author = db.find_one()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: str, db: Collection = Depends(dependencies.get_db)):
    author = db.find_one({"_id": ObjectId(author_id)})

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return author


@router.delete("/{author_id}", status_code=200)
def delete_author(*, author_id: str, db: Collection = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author
    """
    deleted_result = db.delete_one({"_id": ObjectId(author_id)})
    if deleted_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    return {"detail": f"Author id {author_id} deleted successfully"}



@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: str,
    author_in: AuthorUpdate,
    db: Collection = Depends(dependencies.get_db),
):
    update_data = author_in.dict(exclude_unset=True)
    result = db.find_one_and_update(
        {"_id": ObjectId(author_id)},
        {"$set": update_data},
        return_document=True
    )
    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    return result
db = client["your_database_name"]  # Replace with your actual database name

engine = create_engine(DATABASE_URL)


def recreate_database():
    # List of collection names to be created
    collections_to_create = ['authors', 'books', 'publishers']  # Add your collection names

    # Loop through and create collections
    for collection_name in collections_to_create:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
    
    # Here you can also create any required indexes for your collections
    # For example, if you want to create a unique index on the 'username' field in the 'authors' collection:
    # db.authors.create_index([('username', pymongo.ASCENDING)], unique=True)

    # NOTE: MongoDB creates collections implicitly when you insert the first document,
    # so explicitly creating collections is not usually necessary unless you want to set up specific indexes.


@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, db: Collection = Depends(dependencies.get_db)
):
    author_data = author_in.dict()
    result = db.insert_one(author_data)
    if result.inserted_id:
        author_data['_id'] = result.inserted_id
        return author_data
    else:
        raise HTTPException(status_code=500, detail="An error occurred while creating the author.")


recreate_database()

# Dependencies file content
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["your_database_name"]["your_collection_name"]

router = APIRouter()
