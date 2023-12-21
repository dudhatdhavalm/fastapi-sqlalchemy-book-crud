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
from pymongo.database import Database
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from app.schemas.author import AuthorUpdate
from bson import ObjectId
from fastapi import APIRouter, Depends

# Provided imports that we will assume are accessible
# from app import crud
# Assuming dependencies.get_db provides a pymongo.database.Database instance

router = APIRouter()  # In case you haven't initialized it elsewhere

engine = create_engine(DATABASE_URL)


@router.delete("/{author_id}", status_code=200)
def delete_author(*, author_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Author
    """
    authors_collection: Collection = db.get_collection('authors')
    deletion_result = authors_collection.delete_one({'_id': ObjectId(author_id)})
    if deletion_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")
    return {"detail": f"Author id {author_id} deleted successfully"}


# Assuming DATABASE_URL is a MongoDB URI, e.g., "mongodb://localhost:27017/mydatabase"

def recreate_database():
    client = MongoClient(DATABASE_URL)
    db_name = MongoClient(DATABASE_URL).get_default_database()
    
    # Assuming you have 'authors' as a collection equivalent to the 'author' table in SQLAlchemy
    authors_collection = client[db_name].authors
    
    # Here you would recreate indexes and potentially other settings
    # For example, you might have an index on 'name' for authors
    authors_collection.drop_indexes()  # Warning: This will remove all indexes except the default _id index
    authors_collection.create_index('name', unique=True)
    
    # If there are more collections, you can repeat the process for each
    # ...


@router.put("/{author_id}", status_code=200)
def update_author(
    *,
    author_id: str,
    author_in: AuthorUpdate,
    db: Database = Depends(dependencies.get_db),
):
    authors_collection: Collection = db.get_collection("authors")
    result = authors_collection.find_one({"_id": ObjectId(author_id)})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    update_data = author_in.dict(exclude_unset=True)
    authors_collection.update_one({"_id": ObjectId(author_id)}, {"$set": update_data})

    updated_author = authors_collection.find_one({"_id": ObjectId(author_id)})
    return updated_author


@router.get("/{author_id}", status_code=200)
def get_by_id(*, author_id: int, db: MongoClient = Depends(dependencies.get_db)):
    # Assume that 'authors' is the collection where author documents are stored
    # And db_name is the name of the database where this collection exists
    db_name = db.get_default_database().name
    authors_collection: Collection = db[db_name]["authors"]
    
    # In MongoDB, the 'id' might be stored as '_id'
    author = authors_collection.find_one({"_id": author_id})

    if author is None:
        raise HTTPException(status_code=404, detail=f"Author id {author_id} not found")

    # Convert the '_id' field back to 'id' for consistency with the original code behavior, if required.
    # You might need to adjust this line if your document uses a different field or representation for ID.
    author["id"] = author.pop("_id")

    return author


@router.get("", status_code=200)
def get_author(*, db: MongoClient = Depends(dependencies.get_db)):
    # Assuming 'authors' is the collection's name.
    author_collection = db['authors']
    author = author_collection.find_one()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Excluding MongoDB's internal _id from the result, if desired.
    author.pop('_id', None)
    
    return author


recreate_database()

router = APIRouter()


@router.post("", status_code=200)
def create_author(
    *, author_in: AuthorCreate, db: Database = Depends(dependencies.get_db)
):
    # Convert the input model to a dictionary if it is a Pydantic model
    author_dict = author_in.dict() if hasattr(author_in, 'dict') else author_in
    # Insert the new author into the MongoDB database
    result = db.authors.insert_one(author_dict)
    # Retrieve and return the new author
    created_author = db.authors.find_one({"_id": result.inserted_id})
    return created_author
