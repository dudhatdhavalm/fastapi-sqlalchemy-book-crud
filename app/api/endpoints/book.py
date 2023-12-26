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
from pymongo.database import Database
from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.schemas.book import BookUpdate

# Your router goes here. Make sure your router variable is defined:
router = APIRouter()


router = APIRouter()  # I am assuming this has already been defined above


@router.get("/{book_id}", status_code=200)
def get_by_id(*, book_id: str, db: Database = Depends(dependencies.get_db)):
    # Convert string book_id to ObjectId for PyMongo
    try:
        oid = ObjectId(book_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    # Get the book collection and find the document with the provided ObjectId
    book_collection = db.get_collection("books")
    book = book_collection.find_one({"_id": oid})
    
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")

    # Convert the '_id' field from ObjectId to string
    book['_id'] = str(book['_id'])

    return book


@router.delete("/{book_id}", status_code=200)
def delete_book(*, book_id: str, db: Database = Depends(dependencies.get_db)) -> dict:
    """
    Delete Book
    """
    collection = db.get_collection("books")
    result = collection.delete_one({"_id": ObjectId(book_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"detail": f"Book with id {book_id} deleted successfully"}


@router.get("/books/{id}", response_model=Books)
async def find_book(id: str, db: Database = Depends(dependencies.get_db)):
    book = db["books_collection"].find_one({"_id": ObjectId(id)})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    result = jsonable_encoder(book)
    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


@router.put("/{book_id}", status_code=200)
def update_book(
    *,
    book_id: str,  # Assuming book_id is a string representing MongoDB's ObjectId
    book_in: BookUpdate,
    db: MongoClient = Depends(dependencies.get_db)  # Assuming MongoClient is returned here
):
    # Check if the provided book_id is a valid ObjectId
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID format")

    # Convert the string ID to ObjectId for querying
    object_id = ObjectId(book_id)
    
    # Find the existing book
    result = db.books.find_one({'_id': object_id})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Book id {book_id} not found")
    
    # Check if the author exists
    author = db.authors.find_one({'_id': book_in.author_id})
    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )
    
    # Update the book with the supplied data (presuming book_in is a Pydantic model)
    update_data = book_in.dict(exclude_unset=True)
    updated_result = db.books.update_one({'_id': object_id}, {'$set': update_data})
    
    # Check if the update was successful
    if updated_result.matched_count == 1:
        return db.books.find_one({'_id': object_id})
    else:
        raise HTTPException(status_code=500, detail="The book update was not successful")

@router.get("/books", response_model=list[Books])
async def get_books(page_size: int = 10, page: int = 1, db: Database = Depends(dependencies.get_db)):
    if page_size > 100 or page_size < 0:
        page_size = 100
    books_cursor = db["books_collection"].find().skip((page - 1) * page_size).limit(page_size)
    books = list(books_cursor)
    result = jsonable_encoder(books)
    return JSONResponse(status_code=200, content={"status_code": 200, "result": result})

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@router.get("", status_code=200)
def get_book(*, db: Database = Depends(dependencies.get_db)):
    # Assuming 'books' is the collection where book data is stored, including the author embedded or referenced
    # This implementation assumes book documents may contain an 'author' field with embedded author detail.
    # If it's a reference, you have to adjust the query to perform a join (lookup).
    books_collection = db.get_collection('books')
    book = books_collection.find_one()
    if book is not None:
        # Convert ObjectId to string if necessary
        book['_id'] = str(book['_id'])
    return book


def recreate_database():
    client = MongoClient(DATABASE_URL)
    db = client.get_default_database()

    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)


recreate_database()

router = APIRouter()



@router.post("", status_code=200, response_model=Books)
def create_book(
    *, book_in: BookCreate, db: Database = Depends(dependencies.get_db)
) -> Books:
    author_collection = db.get_collection("authors")
    book_collection = db.get_collection("books")

    author = author_collection.find_one({"_id": book_in.author_id})

    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author id {book_in.author_id} not found"
        )

    # Assuming the BookCreate pydantic model can be converted to a dictionary.
    # If not, adjust the dict conversion accordingly.
    book_data = book_in.dict()
    book_data['_id'] = book_collection.insert_one(book_data).inserted_id
    return book_data



















