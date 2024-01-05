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
from app.models.book import BookCollection
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.book import BookCreate, Books
from app.database import get_nosql_db
from bson import ObjectId
from pymongo.database import Database
from fastapi import APIRouter, Depends, HTTPException
from fastapi import HTTPException, status, Depends, APIRouter
from app.schemas.book import BookUpdate
from typing import Any, Dict


@router.get("/books/{book_id}")
def find_book(book_id: str, db: Database = Depends(get_nosql_db)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID")

    book = db.book_collection.find_one({"_id": ObjectId(book_id)})
    if book is not None:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSONable
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": 200, "result": {"book": book}})

router = APIRouter()  # Assuming that router has been initialized earlier in your code

@router.get("/books")
def get_books(page_size: int = 10, page: int = 1, db: Database = Depends(get_nosql_db)):
    if page_size > 100 or page_size < 1:
        page_size = 100

    books_cursor = db.book_collection.find().skip((page - 1) * page_size).limit(page_size)
    books = list(books_cursor)
    for book in books:
        book["_id"] = str(book["_id"])

    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": 200, "result": {"books": books}})


@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: str, db: Database = Depends(get_nosql_db)) -> dict:
    """
    Delete Book using pymongo
    """
    collection = db.get_collection("books")  # replace "books" with the actual name of the collection if different
    result = collection.delete_one({"_id": ObjectId(book_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book id {book_id} not found")

    return {"detail": f"Book id {book_id} deleted successfully"}

engine = create_engine(DATABASE_URL)


@router.put("/{book_id}", status_code=200)
def update_book(
    *,
    book_id: str,
    book_in: BookUpdate,
    db: Database = Depends(get_nosql_db),
) -> Dict[str, Any]:
    # Convert the book_id from string to ObjectId for MongoDB
    oid = ObjectId(book_id)
    updated_book = db['book_collection'].find_one_and_update(
        {"_id": oid}, {"$set": book_in.dict()}, return_document=True
    )

    if not updated_book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

    # The following lines are only applicable if you are also tracking authors as separate entities
    author_id = book_in.author_id  # assuming author_id is available as part of BookUpdate
    author = db['author_collection'].find_one({"_id": ObjectId(author_id)})
    if not author:
        raise HTTPException(
            status_code=404, detail=f"Author with id {book_in.author_id} not found"
        )

    return updated_book


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: str, db: Database = Depends(get_nosql_db)):
    try:
        # In MongoDB, the ID should be wrapped with ObjectId for direct querying
        oid = ObjectId(book_id)
    except:
        # In case the string is not a valid ObjectId, return 404
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found") 
    
    book = db.books.find_one({"_id": oid})

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Convert the '_id' field from ObjectId to string to make it JSON serializable
    book["_id"] = str(book["_id"])
    return book
Session = sessionmaker(bind=engine)


def recreate_database():
    # Connect to the MongoDB server
    client = MongoClient(DATABASE_URL)
   
    # Assuming the DATABASE_URL is mongodb://localhost:27017/mydatabase
    # and you have already defined a BookCollection collection structure, 
    # similar to how you would define models in SQLAlchemy
    
    db_name = 'mydatabase' # Replace with the name of your database
    db = client[db_name]

    # Create collections if they don't exist
    # In MongoDB, collections are created when the first document is inserted,
    # but you can explicitly create them like this if needed, for example, to set collection-level options.
    # Replace 'my_collection' with your actual collection names defined in BookCollection or other models
    if 'my_collection' not in db.list_collection_names():
        db.create_collection('my_collection')

    # Close the connection to the MongoDB server
    client.close()


@router.get("", status_code=200)
def get_book(*, db: Database = Depends(get_nosql_db)):
    books_collection = db.get_collection('books')  # Assuming the collection is named 'books'
    book = books_collection.find_one({"author": "Author Name"})  # Example query for a book with the author 'Author Name'
    if book:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string before returning
        return book
    raise HTTPException(status_code=404, detail="Book not found")


recreate_database()


@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db = Depends(dependencies.get_db)
) -> Books:
    authors_collection = db.authors
    books_collection = db.books

    # Checking if the author exists
    author = authors_collection.find_one({"_id": book_in.author_id})
    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )
    
    # Converting the BookCreate schema to a dictionary and creating the book
    book_data = book_in.dict()
    book_id = books_collection.insert_one(book_data).inserted_id

    # Retrieving the created book
    book = books_collection.find_one({"_id": book_id})
    if not book:
        raise HTTPException(status_code=500, detail="Book creation failed")

    # Returning the created book adhering to the Books schema
    return book

router = APIRouter()



















