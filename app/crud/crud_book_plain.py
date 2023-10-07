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
from pymongo import MongoClient, collection
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.json_util import dumps
from typing import Any, Dict, Union
from bson.json_util import dumps, loads
from datetime import datetime
import pymongo

ModelType = TypeVar("ModelType", bound=Base)
































class CRUDBook:

    def create(self, db: collection.Collection, *, obj_in: BookCreate) -> Dict:
        db_obj = {"title": obj_in.title, "pages": obj_in.pages,
                  "author_id": obj_in.author_id, "created_at": date.today()}
        insertion_result = db.insert_one(db_obj)
        db_obj["_id"] = insertion_result.inserted_id
        return db_obj


    def get_multi(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db.find().skip(skip).limit(limit))

    def get_with_author(self, db: Session) -> List[Book]:
        books = db.query(Book.id, Book.title, Book.pages, Book.created_at,
                         Book.author_id, Author.name.label("author_name")).join(Book, Author.id == Book.author_id).all()
        return books

    
    def get_books_with_id(self, db: MongoClient, book_id: int):
        books = db.books.find({"_id": book_id}, {"author.name": 1, "_id": 1, "title": 1, "pages": 1, "created_at": 1, "author_id": 1})
        response = dumps(books)

        return response


    def update(self, db: pymongo.MongoClient, *, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]) -> Book:
        collection = db['books']
        obj_data = loads(dumps(db_obj.__dict__))
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = vars(obj_in)

        update_data["created_at"] = datetime.now()
        for field in obj_data:
            if field in update_data:
                obj_data[field] = update_data[field]

        collection.replace_one({"_id": db_obj._id}, obj_data)
        updated_obj = collection.find_one({"_id": db_obj._id})
        return Book(**updated_obj)


book_plain = CRUDBook()
