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
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.book import BookCreate
from typing import Any, List, Dict
from typing import Any, Dict, List, Union

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db: MongoClient, *, obj_in: BookCreate) -> dict:

        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": str(obj_in.author_id),
            "created_at": date.today().strftime("%m/%d/%Y")
        }

        result = db.books.insert_one(db_obj)

        if result.acknowledged:
            db_obj["_id"] = str(result.inserted_id)

        return db_obj


    def get(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db.books.find().skip(skip).limit(limit))

    
    def get_with_author(self, db: MongoClient) -> List[Dict[str, Any]]:
        books = db.books.find({}, {"_id": 0, "id": 1, "title": 1, "pages": 1, "created_at": 1, "author_id": 1, "author.name": 1})
        return list(books)


    def get_books_with_id(self, db, book_id: int):
        db = MongoClient().database
        books = db.books.find_one({"_id": ObjectId(book_id)})
        author_name = db.authors.find_one({"_id": books.get("author_id")}).get("name")
        books["author_name"] = author_name

        return books


    def update(self, db: MongoClient, *, db_obj: str, obj_in: Dict[str, Any]) -> dict:
        db_obj_id = ObjectId(db_obj)
        result = db.books.update_one({'_id': db_obj_id}, {"$set": obj_in})
        if result.matched_count:
            return db.books.find_one({'_id': db_obj_id})
        else:
            return None


book = CRUDBook(Book)
