from datetime import date
from typing import Optional
from app import crud
from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.book import BookCreate, Books, BookUpdate
from app.models.book import Base
from app.settings import DATABASE_URL
from app.api import dependencies
from pymongo import MongoClient
from app.settings import MONGO_DB_URL  # Replace this with your MongoDB database URL.
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    client = MongoClient(MONGO_DB_URL)  # Connect to the MongoDB server using the connection string.
    db = client.get_default_database()  # Get the default database.
    collection_names = db.list_collection_names()  # Get a list of all collection names in the database.

    for name in collection_names:
        db.drop_collection(name)  # Delete each collection

    # Recreate collections if needed. 
    # In MongoDB collections do not need to be explicitly created, 
    # they are created when the first document is inserted.


recreate_database()

router = APIRouter()


@router.post("", status_code=200, response_model=Books)
def create_book(*, book_in: BookCreate, db: Session = Depends(dependencies.get_db)) -> Books:
    book = crud.book_plain.create(db=db, obj_in=book_in)
    return book


@router.get("", status_code=200)
def get_book(*, db: Session = Depends(dependencies.get_db)):
    book = crud.book_plain.get_with_author(db=db)
    return book


@router.get("/{id}", status_code=200)
def get_by_id(*, book_id: int, db: Session = Depends(dependencies.get_db)):
    book = crud.book_plain.get_books_with_id(db=db, book_id=book_id)
    return book


@router.put("/{id}", status_code=200)
def update_book(*, request: Request, book_id: int, book_in: BookUpdate, db: Session = Depends(dependencies.get_db)):
    result = crud.book.get(db=db, id=book_id)
    book = crud.book_plain.update(db=db, db_obj=result, obj_in=book_in)
    return book


















