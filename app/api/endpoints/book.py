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
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.book import BookCreate, Books
from app.crud import author_plain, book_plain
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from app.schemas.book import BookUpdate
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.collection import Collection

# Assuming router and dependencies have been appropriately defined elsewhere.
router = APIRouter()

engine = create_engine(DATABASE_URL)


@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: str, db_client: MongoClient = Depends(dependencies.get_db_client)) -> dict:
    """
    Delete Book
    """
    collection = db_client["your_database_name"]["books"]
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")
    return {"detail": f"Book id {book_id} deleted successfully"}


@router.get("/books/{book_id}")
def find_book(book_id: str, db_client: MongoClient = Depends(dependencies.get_db_client)):
    try:
        object_id = ObjectId(book_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID")
    
    db = db_client.get_database()
    books: Collection = db.books
    book = books.find_one({"_id": object_id})
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    result = jsonable_encoder({"book": book})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": 200, "result": result})
Session = sessionmaker(bind=engine)

@router.get("/books")
def get_books(page_size: int = 10, page: int = 1, db_client: MongoClient = Depends(dependencies.get_db_client)):
    if page_size > 100 or page_size < 0:
        page_size = 100

    db = db_client.get_database()
    books: Collection = db.books
    books_list = books.find().skip((page - 1) * page_size).limit(page_size)
    
    result = jsonable_encoder({"books": list(books_list)})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status_code": 200, "result": result})


@router.put("/{book_id}", status_code=200)
def update_book(
    *,
    book_id: str,  # Assume book_id is a string representation of MongoDB's ObjectId
    book_in: BookUpdate,
    db_client: MongoClient = Depends(dependencies.get_db_client),
):
    db = db_client.get_database()  # Adapt to match your database name access method
    book_collection = db.get_collection("books")  # Replace with your book collection name
    author_collection = db.get_collection("authors")  # Replace with your author collection name

    book = book_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    author = author_collection.find_one({"_id": book_in.author_id})
    if not author:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    # Prepare the update data, converting the BookUpdate pydantic model to a dictionary
    update_data = book_in.dict(exclude_unset=True)
    # Perform the update in the database
    updated_book = book_collection.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$set": update_data},
        return_document=True
    )
    if not updated_book:
        raise HTTPException(status_code=500, detail="Book update failed")

    return updated_book


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db_name = client.get_database()  # You need to specify the database name in the DATABASE_URL or here
    client.drop_database(db_name)


# Assuming the books are stored in a collection named 'books' and have an 'author' field to join with the 'authors' collection.

@router.get("", status_code=200)
def get_book(*, db_client: MongoClient = Depends(dependencies.get_db_client)):
    # Assuming your database is called 'library', adjust the name accordingly if it's different.
    db = db_client.library
    # Assuming the books are in a collection named 'books', with embedded author documents
    books_with_authors = db.books.find({}, {'_id': 0})  # Change projection as needed, this example removes the _id field from results
    # Converting cursor to list as FastAPI cannot directly return a cursor object
    book_list = list(books_with_authors)
    if not book_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
    return book_list


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: str, db_client: MongoClient = Depends(dependencies.get_db_client)):
    # Assuming the collection name is 'books' and is fetched from some dependency
    db = db_client.get_default_database()
    books_collection = db.books
    
    # Convert book_id to ObjectId if it's in valid ObjectId format, otherwise raise exception
    try:
        oid = ObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    book = books_collection.find_one({"_id": oid})

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Assuming that the function will convert MongoDB's _id field to a string called id,
    # and that the book document is compatible with the response model.
    book["id"] = str(book["_id"])
    del book["_id"]

    return book


recreate_database()

router = APIRouter()


@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db_client: MongoClient = Depends(dependencies.get_db_client)
) -> Books:
    author = author_plain.get_by_author_id(db_client=db_client, id=book_in.author_id)

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    book = book_plain.create(db_client=db_client, obj_in=book_in.dict())
    return book



















