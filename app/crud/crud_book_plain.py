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
from typing import List
from bson.json_util import dumps
from bson.objectid import ObjectId
from typing import Any, Dict, Union
from pymongo import MongoClient, collection
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["database_name"]
collection = db["collection_name"]

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: MongoClient, *, obj_in: BookCreate) -> Book:
        book_dict = obj_in.dict()
        book_dict['created_at'] = date.today()
        result = db.books.insert_one(book_dict)
        book_dict["_id"] = str(result.inserted_id)

        return Book(**book_dict)


    def get_multi(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.books.find().skip(skip).limit(limit)


    def get_with_author(self, db: MongoClient) -> List[Book]:
        books_with_author = list(db['book'].aggregate([
            {
                "$lookup":
                    {
                        "from": "authors",
                        "localField": "author_id",
                        "foreignField": "_id",
                        "as": "author_docs"
                    }
            },
            {
                "$project":
                    {
                        "_id": 1,
                        "title": 1,
                        "pages": 1,
                        "created_at": 1,
                        "author_id": 1,
                        "author_name": "$author_docs.name"
                    }
            }
        ]))
        return dumps(books_with_author)


    def get_books_with_id(self, db: MongoClient, book_id: str):
        books = db.book.find_one({"_id": ObjectId(book_id)},
                                 {"_id": 1, "title": 1, "pages": 1, "created_at": 1, "author_id": 1, "author_name": 1})

        return books


    def update(self, book_id: str, *, obj_in: Union[Book, Dict[str, Any]]) -> Dict[str, Any]:
        # Convert obj_in to dict based on its type
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Add timestamp to the update_data
        update_data["created_at"] = datetime.now()

        # Parse the book_id to ObjectId format
        book_id = {
            "_id": ObjectId(book_id)
        }

        # Update the document in MongoDB
        updated_book = collection.find_one_and_update(book_id, {'$set': update_data}, return_document=True)
        return updated_book


book_plain = CRUDBook()
