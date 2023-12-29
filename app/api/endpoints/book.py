from datetime import date
from typing import Optional
from app import crud
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.book import BookCreate, Books, BookUpdate
from app.models.book import Base
from app.settings import DATABASE_URL
from app.api import dependencies
from fastapi.exceptions import RequestValidationError
from pymongo import MongoClient
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate, Books
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from app.schemas.book import Books
from app.schemas.book import BookUpdate

router = APIRouter()  # Assuming router is defined somewhere globally

# from fastapi import APIRouter, Depends, HTTPException, status
# from app.api import dependencies
# from pymongo.database import Database
# from bson import ObjectId

@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: str, db: Database = Depends(dependencies.get_db)):
    # Find the book by its ID, converting the string to an ObjectId
    book = db.books.find_one({"_id": ObjectId(book_id)})
    
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Convert the _id from ObjectId to str for JSON serialization
    book['_id'] = str(book['_id'])
    return book


@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Book
    """
    # Assuming book_id is the string representation of ObjectId
    book_id_obj = ObjectId(book_id)
    result = db.books.delete_one({"_id": book_id_obj})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    return {"detail": f"Book id {book_id} deleted successfully"}

@router.get("/books/{id}")
def find_book(id: str, db: Database = Depends(dependencies.get_db)):
    book = db['books'].find_one({"_id": ObjectId(id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book['id'] = str(book['_id'])
    del book['_id']

    result = jsonable_encoder({"book": book})
    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@router.put("/{book_id}", status_code=200)
async def update_book(
    *,
    book_id: str,
    book_in: BookUpdate,
    db: Database = Depends(dependencies.get_db),
):
    collection = db.books  # assuming your books are stored in a collection called 'books'

    # First, ensure the book exists
    book = await collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Assuming you also need to check for the existence of the author
    author = await db.authors.find_one({"_id": ObjectId(book_in.author_id)})
    if not author:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    # Convert book_update schema to a dictionary, excluding any non-updated fields
    update_data = {k: v for k, v in book_in.dict().items() if v is not None}

    # Perform the update
    result = await collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Update operation failed")

    # After updating, return the updated book object
    updated_book = await collection.find_one({"_id": ObjectId(book_id)})

    return updated_book

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db_name = client.get_default_database().name  # Assuming you have a default database configured in the URL
    
    # Drop the database if it exists
    client.drop_database(db_name)
    
    # In pymongo, the database will be created automatically when a new document is inserted
    # No explicit database creation command is required


recreate_database()


@router.get("", status_code=200)
def get_book(*, db: Database = Depends(dependencies.get_db)):
    # Assuming that there is a collection named 'books' and it contains the author information embedded or as a reference.
    books_collection = db.books
    books_with_authors = list(books_collection.find({}))

    # Convert the _id field to string, as PyMongo returns it as an ObjectId
    books_with_authors = [
        {
            **book,
            '_id': str(book['_id']),  # convert ObjectId to string for JSON serialization
            'author_id': str(book['author_id']) if 'author_id' in book and isinstance(book['author_id'], ObjectId) else book.get('author_id', None)
        }
        for book in books_with_authors
    ]
    
    # Convert the list of books with authors to Pydantic models (if necessary)
    book_models = [Books(**book_data) for book_data in books_with_authors]

    return book_models

router = APIRouter()


# Assuming 'crud.author_plain.get_by_author_id' and 'crud.book_plain.create' should be replaced as well.
# The following code will use MongoClient to interact with a MongoDB database.
# Make sure to replace 'mongo_db' and 'authors_collection' and 'books_collection' with the actual names of your database and collections.

@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db: MongoClient = Depends(dependencies.get_db)
) -> Books:
    # Adjust the following line to use your actual MongoDB authors collection name
    author = db.authors_collection.find_one({'_id': book_in.author_id})

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    # Transform the BookCreate pydantic model to a dictionary for MongoDB insertion
    book_data = book_in.dict()
    
    # Adjust the following line to use your actual MongoDB books collection name
    result = db.books_collection.insert_one(book_data)

    # After inserting, retrieve the inserted document back from MongoDB using result.inserted_id
    # to return the book as specified by the response_model
    book = db.books_collection.find_one({'_id': result.inserted_id})

    return book  # Book should conform to the Books Pydantic model defined in response_model



















