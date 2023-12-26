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
from typing import List, Dict
import json

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db_collection: Collection, *, obj_in: dict) -> dict:
        obj_in_data = obj_in.dict(by_alias=True) if hasattr(obj_in, 'dict') else obj_in
        obj_in_data["created_at"] = datetime.utcnow()
        
        result = db_collection.insert_one(obj_in_data)
        created_book = db_collection.find_one({"_id": result.inserted_id})
        return created_book


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))


    def get_with_author(self, db: Collection) -> List[Dict]:
        pipeline = [
            {
                "$lookup": {
                    "from": "authors",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_info"
                }
            },
            {
                "$unwind": "$author_info"
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"
                }
            }
        ]
        books_with_authors = list(db.aggregate(pipeline))
        return books_with_authors


    def get_books_with_id(self, db: Collection, book_id: int):
        # Assuming the book_id is stored as an integer in MongoDB, if it's stored as a string, convert it accordingly.
        book = db.find_one({
            "_id": book_id
        }, {
            "title": 1,
            "pages": 1,
            "created_at": 1,
            "author_id": 1
        })

        # Fetch the author details from the 'authors' collection.
        # Assuming there's an 'authors' collection and 'author_id' field in the books documents corresponds to '_id' in authors.
        if book and "author_id" in book:
            author = db.database["authors"].find_one({"_id": book["author_id"]})
            if author:
                book["author_name"] = author.get("name")

        # The below is not strictly necessary as pymongo returns a dictionary that is already json-serializable.
        # But if you need to modify the result or ensure certain formatting, you could use jsonable_encoder from FastAPI.
        # from fastapi.encoders import jsonable_encoder
        # book = jsonable_encoder(book)

        return book


    def update(self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[dict, Dict[str, Any]]) -> dict:
        if isinstance(db_obj_id, ObjectId):
            filter_query = {'_id': db_obj_id}
        else:
            # When db_obj_id is not an instance of ObjectId, it might be a string that needs to be converted.
            # Here we safely convert string ids to ObjectId, if it is not already in that format.
            filter_query = {'_id': ObjectId(db_obj_id)}

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = json.loads(obj_in.json(exclude_unset=True))

        # $set is used in MongoDB to update fields in the document.
        updated_result = db.find_one_and_update(filter_query, {'$set': update_data}, return_document=True)

        return updated_result


book_plain = CRUDBook()
