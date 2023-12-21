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
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from typing import List
from typing import Dict, Any

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, collection: Collection, *, obj_in: dict) -> dict:
        book_data = {
            "title": obj_in['title'],
            "pages": obj_in['pages'],
            "author_id": ObjectId(obj_in['author_id']),
            "created_at": datetime.utcnow()
        }
        result = collection.insert_one(book_data)
        new_book = collection.find_one({"_id": result.inserted_id})
        return new_book

    
    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        cursor = collection.find().skip(skip).limit(limit)
        books = list(cursor)
        return books


    def get_with_author(self, db: Collection) -> List[dict]:
        # Using an aggregation pipeline to perform the join operation
        pipeline = [
            {
                "$lookup": {
                    "from": "authors",  # assuming the authors collection is named "authors"
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_info"
                }
            },
            {
                "$unwind": "$author_info"  # Deconstruct the array field from the lookup
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"  # Project the author's name
                }
            }
        ]
        books = list(db.aggregate(pipeline))
        return books

    def get_books_with_id(self, db: Collection, book_id: int):
        book = db.find_one({"_id": ObjectId(book_id)}, {"_id": 1, "title": 1, "pages": 1, "created_at": 1, "author_id": 1})

        if not book or "author_id" not in book:
            return None 

        author = db.database['author'].find_one({"_id": book["author_id"]}, {"name": 1})
        
        if author:
            book["author_name"] = author.get("name")
        
        return book


    def update(self, collection: Collection, *, db_obj_id: str, obj_in: Dict[str, Any]) -> Dict:
        if isinstance(obj_in, dict):
            update_data = {k: v for k, v in obj_in.items() if v is not None}
            
            # If you want the updated_at field to be changed when an update occurs
            # uncomment the following line:
            # update_data['updated_at'] = datetime.utcnow()
            
            result = collection.find_one_and_update(
                {"_id": ObjectId(db_obj_id)},
                {"$set": update_data},
                return_document=True
            )
            return result
        else:
            # Implement other cases or error handling depending on your requirements
            raise Exception('obj_in must be a dictionary')


book = CRUDBook(Book)
