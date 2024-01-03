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
from app.settings import MONGODB_URL
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.book import BookCreate, Books
from pymongo.database import Database
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import HTTPException, status, Depends, APIRouter
from app.schemas.book import BookUpdate
from bson import ObjectId

# Assuming you have settings already configured with the MongoDB URL
client = MongoClient(MONGODB_URL)
db = client.get_default_database()  # Or specify your database name


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(*, book_id: int, db: Database = Depends(dependencies.get_mongo_db)) -> dict:
    """
    Delete Book by ID using PyMongo
    """
    delete_result = db.books.delete_one({"_id": book_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {book_id} not found"
        )
    
    return {"detail": f"Book with id {book_id} deleted successfully"}


@router.get("/books/{book_id}")
def find_book(book_id: str, db: Database = Depends(dependencies.get_mongo_db)):
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    result = jsonable_encoder({"book": book})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": status.HTTP_200_OK, "result": result})


# Modified function with pymongo
@router.put("/{book_id}", status_code=200)
def update_book(
    *,
    book_id: int,
    book_in: BookUpdate,
    db: Database = Depends(dependencies.get_mongo_db),
):
    # Assuming the collection is named 'books' and it's a Pydantic model, not just a dictionary
    book_collection = db.get_collection('books')

    # Find the book by ID
    book = book_collection.find_one({'_id': book_id})
    if not book:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Find the author by ID (assuming authors are in the 'authors' collection)
    author_collection = db.get_collection('authors')
    author = author_collection.find_one({'_id': book_in.author_id})
    if not author:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    # Update the book details where book_in is converted to a dictionary
    update_data = book_in.dict(exclude_unset=True)
    book_collection.update_one({'_id': book_id}, {'$set': update_data})
    book.update(update_data)

    return book

@router.get("/books")
def get_books(page_size: int = 10, page: int = 1, db: Database = Depends(dependencies.get_mongo_db)):
    if page_size > 100 or page_size < 0:
        page_size = 100

    books = list(db.books.find().skip((page - 1) * page_size).limit(page_size))
    result = jsonable_encoder({"books": books})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": status.HTTP_200_OK, "result": result})


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: int, db: Database = Depends(dependencies.get_mongo_db)):
    book_collection = db.get_collection('books')
    book = book_collection.find_one({'_id': book_id})

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

    return book


@router.get("", status_code=200)
def get_book(*, db: Database = Depends(dependencies.get_mongo_db)):
    books_collection = db['books']  # Name of the collection to be used, adjust if your collection has a different name
    authors_collection = db['authors']  # Name of the collection containing authors, adjust as needed

    # Assuming a document book references an author with field 'author_id'
    # And that author_id is the same as _id in authors collection
    # We will perform a 'join' like operation, similar to what get_with_author would be doing in SQLAlchemy
    result = []
    for book in books_collection.find():  # Replace find() with appropriate query if needed
        # Fetch the author for the current book
        author = authors_collection.find_one({'_id': book['author_id']})
        book_with_author = {**book, 'author': author}  # Merge the book info with its author
        result.append(book_with_author)

    return result

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db: Database = Depends(dependencies.get_mongo_db)
) -> Books:
    # Replace CRUD operation with pymongo operation
    authors_collection = db.get_collection('authors')
    books_collection = db.get_collection('books')

    # Convert the BookCreate Pydantic model to a dictionary and exclude unset values
    book_dict = book_in.dict(exclude_unset=True)

    # Attempt to find the author in the authors collection by their ID
    author = authors_collection.find_one({"_id": book_dict['author_id']})

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_dict['author_id']} not found"
        )

    # Insert the new book into the books collection
    book_id = books_collection.insert_one(book_dict).inserted_id

    # Retrieve the inserted book using the newly obtained ID
    book = books_collection.find_one({"_id": book_id})
    
    # Return the book data in response
    return book


def recreate_database():
    # In MongoDB, to 'recreate' a database, you'd drop it, and it gets created automatically on the next write
    db_name = db.name  # Store the name before dropping
    client.drop_database(db_name)
    # The database will be recreated with the first new insert operation


recreate_database()

router = APIRouter()



















