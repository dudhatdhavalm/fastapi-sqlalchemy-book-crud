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
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    client = MongoClient(DATABASE_URL)
    # Un-comment the below lines if you wish to drop the db first. 
    # Be careful as it deletes everything in the db.
    # for name in client.list_database_names():
    #     client.drop_database(name)

    # In mongoDB, there's technically no need to "create" a database.
    # A database is automatically created when you start inserting data into it.
    # The following line is just to demonstrate that you can get or create a db.
    db = client.get_database('books_db')  # This creates a new database named 'books_db' if it doesn't exist.


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


















