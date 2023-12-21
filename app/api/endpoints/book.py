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
from app.settings import DATABASE_URL  # Assuming this contains the MongoDB connection string
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from app.schemas.book import BookCreate, Books
from bson import ObjectId
from app.crud.book_plain import get_with_author as get_with_author_plain
from fastapi import HTTPException, Depends, APIRouter
from fastapi import HTTPException, Depends, APIRouter, status
from app.schemas.book import BookUpdate

router = APIRouter()  # Assuming this instance exists in your code base



@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Book
    """
    deleted_count = db.books.delete_one({"_id": ObjectId(book_id)}).deleted_count
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book id {book_id} not found"
        )
    return {"detail": f"Book id {book_id} deleted successfully"}



#@router.get("/books/{id}")
def find_book(id: str, db: Database = Depends(dependencies.get_db)):
    book = db["books"].find_one({"_id": ObjectId(id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}

router = APIRouter()  # Assumed to be missing in the provided code snippet


#@router.get("/books")
def get_books(page_size: int = 10, page: int = 1, db: Database = Depends(dependencies.get_db)):
    if page_size > 100 or page_size < 1:
        raise HTTPException(status_code=400, detail="Invalid page size")

    skip_amount = (page - 1) * page_size
    books_cursor = db["books"].find().skip(skip_amount).limit(page_size)
    books = list(books_cursor)

    return {"books": books}


#@router.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status_code": 500, "message": str(exc)},
    )


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
def update_book(
    *,
    book_id: str,
    book_in: BookUpdate,
    db: Database = Depends(dependencies.get_db),  # Now the dependency is set to use PyMongo
):
    books_collection = db.get_collection("books")  # Replace with your actual books collection name
    authors_collection = db.get_collection("authors")  # Replace with your actual authors collection name

    # Verify the book exists
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book id {book_id} not found")

    # Verify the author exists
    author = authors_collection.find_one({"_id": ObjectId(book_in.author_id)})
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Author id {book_in.author_id} not found"
        )

    # Update book
    updated_book = {k: v for k, v in book_in.dict().items() if v is not None}
    books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_book})

    # Retrieve the updated book
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    
    return book


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: str, db: Database = Depends(dependencies.get_db)):
    # Convert book_id to a proper ObjectId
    try:
        object_id = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    # Use the PyMongo query to find the book by its '_id'
    book = db.books.find_one({"_id": object_id})

    # If the book does not exist, raise an HTTPException
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # PyMongo returns a dictionary that contains ObjectId which is not JSON serializable,
    # so we need to convert '_id' to string before returning
    book['_id'] = str(book['_id'])

    return book

# Assuming this code is part of a larger FastAPI application, the router should be defined elsewhere
router = APIRouter() 

client = MongoClient(DATABASE_URL)


@router.get("", status_code=200)
def get_book(*, db: Database = Depends(dependencies.get_db)):
    # Assuming 'get_with_author_plain' function is similar to 'crud.book_plain.get_with_author'
    # but implemented with PyMongo and the book collection is named 'books'
    books_collection = db.get_collection('books')
    
    # Use PyMongo to perform a similar query
    # Assuming that the function 'get_with_author_plain' will handle the logic
    # to retrieve a book with author details as needed
    book = get_with_author_plain(db=books_collection)

    # Return the book, will need to convert ObjectId to string if it's returned in the response
    def serialize(book):
        if book and '_id' in book:
            book['_id'] = str(book['_id'])
        return book

    return serialize(book)
db = client.get_default_database()  # Replace with your specific database name if needed

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db: Database = Depends(dependencies.get_db)  # Change the dependency to use pymongo
) -> Books:
    # Adapt the get_by_author_id function to use MongoDB
    author = crud.author_plain.get_by_author_id(db=db, id=book_in.author_id)

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )
    
    # Convert a Pydantic model to a dictionary
    book_data = book_in.dict()
    
    # Insert the new book data into the MongoDB collection
    book_collection = db["books"]  # Assuming you have a books collection
    inserted_id = book_collection.insert_one(book_data).inserted_id

    # Read the inserted data back from Mongo to return it
    created_book = book_collection.find_one({"_id": inserted_id})
    
    # Assuming you have a function to convert a Mongo document into a Pydantic model
    return crud.book_plain.create_mongo_to_model(created_book)


def recreate_database():
    # List all collections
    collection_names = db.list_collection_names()
    # Drop each collection
    for collection in collection_names:
        db.drop_collection(collection)
    # There is no need to explicitly create collections with pymongo
    # as they will be created automatically when documents are inserted.


recreate_database()

router = APIRouter()



















