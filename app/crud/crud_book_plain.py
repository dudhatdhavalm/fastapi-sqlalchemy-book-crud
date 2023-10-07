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
from typing import Any, Dict, Union
from bson import ObjectId

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: MongoClient, *, obj_in: BookCreate) -> Dict:
        collection = db['books']
        data = {"title": obj_in.title,
                "pages": obj_in.pages,
                "author_id": ObjectId(obj_in.author_id),
                "created_at": date.today()}
        result = collection.insert_one(data)
        return collection.find_one({"_id": result.inserted_id})


    def get_multi(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db['books'].find().skip(skip).limit(limit))


    def get_with_author(self, db) -> List[Dict]:
        books = list(db.books.aggregate([
            {"$lookup": 
                {
                    "from": "authors",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_data"
                }
            },
            {"$unwind": "$author_data"},
            {"$project": 
                {
                    "_id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_data.name"
                }
            }
        ]))

        for book in books:
            # Convert ObjectIds to string
            book["_id"] = str(book["_id"])
            book["author_id"] = str(book["author_id"])

        return books


    def get_books_with_id(self, db: MongoClient, book_id: int):
        books = db.books.find_one(
            {"_id": ObjectId(book_id)},
            {"title": 1, "pages": 1, "created_at": 1, "author_id": 1, "_id": 0}
        )
        
        if books and "author_id" in books:
            author = db.authors.find_one({"_id": ObjectId(books["author_id"])})
            if author:
                books["author_name"] = author.get("name")

        return books


    def update(self, *, db_obj_id: str, obj_in: Union[Book, Dict[str, Any]]) -> Dict:
        collection = self.db['books']
        book = collection.find_one({"_id": ObjectId(db_obj_id)})
        if book is None:
            return

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["created_at"] = date.today()
        book.update(update_data)

        collection.save(book)
        return book


book_plain = CRUDBook()
