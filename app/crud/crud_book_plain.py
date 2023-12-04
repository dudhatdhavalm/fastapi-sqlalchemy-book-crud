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
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: Collection, *, obj_in: BookCreate) -> Dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": obj_in.author_id,
            "created_at": datetime.utcnow()
        }
        result = db.insert_one(db_obj)
        return db.find_one({"_id": result.inserted_id})


    def get(self, db: MongoClient, collection: str, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        collection: Collection = db[collection]
        return list(collection.find().skip(skip).limit(limit))


    def get_with_author(self, db: Collection) -> List[Dict[str, Union[str, Any]]]:
        books = list(
            db.aggregate([
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
                        "_id": 0,
                        "id": "$_id",
                        "title": 1,
                        "pages": 1,
                        "created_at": {
                            "$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$created_at"}
                        },
                        "author_id":"$author._id",
                        "author_name": "$author.name",
                    }
                }
            ])
        )
        return books


    def get_books_with_id(self, db: MongoClient, book_id: int) -> Dict[str, Any]:
        books = db.Books.find_one({"_id": ObjectId(book_id)}, {"title": 1, "pages": 1, "created_at": 1, "author_id": 1, "_id": 0})

        if books is not None:
            author = db.Authors.find_one({"_id": ObjectId(books["author_id"])}, {"name": 1, "_id": 0})
            if author is not None:
                books["author_name"] = author["name"]
                
        return books


    def update(
        self, db: MongoClient, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]
    ) -> Dict[str, Any]:
        collection: Collection = db["books"]
        obj_data = db_obj
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                obj_data[field] = update_data[field]
                
        update_result = collection.update_one({"_id": ObjectId(obj_data['_id'])}, {"$set": obj_data})

        if update_result.matched_count > 0:
            updated_book = collection.find_one({"_id": ObjectId(obj_data['_id'])})
            return updated_book
        else:
            return None


book_plain = CRUDBook()
