from typing import Any, Dict, List, TypeVar, Union
from app.models.book import Book
from app.models.author import Author
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.db.base_class import Base
from datetime import date

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBook:
    def create(self, db: Session, *, obj_in: BookCreate) -> Book:
        db_obj = Book(title=obj_in.title, pages=obj_in.pages,
                      author_id=obj_in.author_id)
        db_obj.created_at = date.today()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.query(Book).offset(skip).limit(limit).all()

    def get_with_author(self, db: Session) -> List[Book]:
        books = db.query(Book.id, Book.title, Book.pages, Book.created_at,
                         Book.author_id, Author.name.label("author_name")).join(Book, Author.id == Book.author_id).all()
        return books

    def get_books_with_id(self, db: Session, book_id: int):
        books = db.query(Book.id, Book.title, Book.pages, Book.created_at,
                         Book.author_id, Author.name.label("author_name")).join(Book, Author.id == Book.author_id).filter(Book.id == book_id).first()

        return books

    def update(self, db: Session, *, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]) -> Book:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["created_at"] = date.today()
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


book_plain = CRUDBook()
