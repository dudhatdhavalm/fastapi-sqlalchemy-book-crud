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
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.book import BookCreate, Books
from app.crud import author_plain, book_plain
from pymongo import MongoClient
from app.crud import book_plain
from app.schemas.book import BookUpdate
from fastapi import APIRouter

# Connecting to MongoDB
client = MongoClient(DATABASE_URL)
db = client.test_database

client = MongoClient('mongodb_url')
db = client['db_name']


@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: int, db: MongoClient = Depends(dependencies.get_db)) -> dict:
    """
    Delete Book
    """
    result = db.books.delete_one({"_id": book_id})
    if result.deleted_count:
        return {"detail": f"Book id {book_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")


@router.get("/books/{id}")
def find_book(id: int, db: MongoClient = Depends(dependencies.get_db)):
    book = db.books.find_one({"_id": id})
    if book is None:
        return JSONResponse(status_code=404, content={"status_code": 404, "message": "Book not found"})

    result = jsonable_encoder({"book": book})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@router.put("/{book_id}", status_code=200)
def update_book(
    *,
    book_id: int,
    book_in: BookUpdate,
    db: MongoClient = Depends(dependencies.get_db),
):
    book_collection = db["book"]
    author_collection = db["author"]

    result = book_collection.find_one({"_id": book_id})

    if result is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    author = author_collection.find_one({"_id": book_in.author_id})
    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    updated_book = book_in.dict(exclude_unset=True)
    book_collection.update_one({"_id": book_id}, {"$set": updated_book})

    return {"detail": "Book successfully updated"}

@router.get("/books")
def get_books(page_size: int = 10, page: int = 1, db: MongoClient = Depends(dependencies.get_db)):
    if page_size > 100 or page_size < 0:
        page_size = 100

    books = list(db.books.find().limit(page_size).skip((page - 1) * page_size))

    result = jsonable_encoder({"books": books})

    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})

engine = create_engine(DATABASE_URL)


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: int, db: MongoClient = Depends(dependencies.get_db)):
    collection = db["book"]
    book = collection.find_one({"_id": book_id})

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    return book
Session = sessionmaker(bind=engine)

def recreate_database():
	pass


recreate_database()



@router.get("", status_code=200)
def get_book():
    book_collection = db['book_collection']
    book_document = book_collection.find_one({"author": {"$exists": True}})
    book = book_plain.get_with_author(book_document)
    return book

router = APIRouter()


@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db=Depends(dependencies.get_db)
) -> Books:
    author = author_plain.get_by_author_id(id=book_in.author_id)

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    book = book_plain.create(obj_in=book_in)
    return book



















