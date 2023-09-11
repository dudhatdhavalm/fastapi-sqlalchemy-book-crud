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
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

router = APIRouter()


@router.post("", status_code=200, response_model=Books)
def create_book(*, book_in: BookCreate, db: Session = Depends(dependencies.get_db)) -> Books:
    book = crud.book.create(db=db, obj_in=book_in)
    return book


@router.get("", status_code=200)
def get_book(*, db: Session = Depends(dependencies.get_db)):
    book = crud.book.get_with_author(db=db)
    return book


@router.get("/{id}", status_code=200)
def get_by_id(*, book_id: int, db: Session = Depends(dependencies.get_db)):
    book = crud.book.get_books_with_id(db=db, book_id=book_id)
    return book


@router.put("/{id}", status_code=200)
def update_book(*, request: Request, book_id: int, book_in: BookUpdate, db: Session = Depends(dependencies.get_db)):
    result = crud.book.get(db=db, id=book_id)
    book = crud.book.update(db=db, db_obj=result, obj_in=book_in)
    return book

# @router.get("/books/{id}")
# def find_book(id: int):
#     session = Session()
#     book = session.query(Book).filter(Book.id == id).first()
#     session.close()

#     result = jsonable_encoder({"book": book})

#     return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


# @router.get("/books")
# def get_books(page_size: int = 10, page: int = 1):
#     if page_size > 100 or page_size < 0:
#         page_size = 100

#     session = Session()
#     books = session.query(Book).limit(
#         page_size).offset((page - 1) * page_size).all()
#     session.close()

#     result = jsonable_encoder({"books": books})

#     return JSONResponse(status_code=200, content={"status_code": 200, "result": result})


# @router.put("/books")
# def update_book(id: int, title: Optional[str] = None, pages: Optional[int] = None):
#     session = Session()
#     book = session.query(Book).get(id)
#     if title is not None:
#         book.title = title
#     if pages is not None:
#         book.pages = pages
#     session.commit()
#     session.close()

#     return JSONResponse(
#         status_code=200, content={"status_code": 200, "message": "success"}
#     )


# @router.delete("/books")
# def delete_book(id: int):
#     session = Session()
#     book = session.query(Book).get(id)
#     session.delete(book)
#     session.commit()
#     session.close()

#     return JSONResponse(
#         status_code=200, content={"status_code": 200, "message": "success"}
#     )


# @router.exception_handler(Exception)
# def exception_handler(request, exc):
#     json_resp = get_default_error_response()
#     return json_resp


# def get_default_error_response(status_code=500, message="Internal Server Error"):
#     return JSONResponse(
#         status_code=status_code,
#         content={"status_code": status_code, "message": message},
#     )
