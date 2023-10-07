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
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Any, Dict, Union
from pymongo import MongoClient, collection

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db: MongoClient, *, obj_in: Dict) -> Dict:
        obj_in["created_at"] = datetime.today()
        result = db.books.insert_one(obj_in)
        return db.books.find_one({"_id": result.inserted_id})


    def get_multi(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db.books.find().skip(skip).limit(limit))


    def get_with_author(self, db: MongoClient) -> List[Dict]:
        pipeline = [
            {
                "$lookup": {
                    "from": "author",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author"
                }
            },
            {
                "$project": {
                    "id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author.name"
                }
            }
        ]
        books = db['book'].aggregate(pipeline)
        return list(books)


    def get_books_with_id(self, db: Database, book_id: int):
        books = db.books.find_one({"id": book_id}, {"id": 1, "title": 1, "pages": 1, 
                                            "created_at": 1, "author_id": 1, "author_name": 1})

        return books

    def update(self, db: collection.Collection, *, db_obj: Dict[str, Any], obj_in: Union[Book, Dict[str, Any]]) -> Dict:
        db_obj["created_at"] = datetime.today()
        updated_book = db.find_one_and_update(
            {"_id": db_obj["_id"]}, 
            {"$set": obj_in}, 
            return_document=True)
        if updated_book:
            return updated_book
        else:
            raise Exception('Book not found')   # add appropriate error handling as needed


book = CRUDBook(Book)
