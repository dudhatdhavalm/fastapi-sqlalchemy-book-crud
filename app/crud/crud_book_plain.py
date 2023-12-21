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
from datetime import datetime
from bson import ObjectId
from typing import List
from typing import Dict, Any
from typing import Union, Dict, Any

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, collection: Collection, *, obj_in: BookCreate) -> dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": ObjectId(obj_in.author_id),
            "created_at": datetime.utcnow()
        }
        result = collection.insert_one(db_obj)
        # Return the newly created book with its ID
        return {"_id": result.inserted_id, **db_obj}

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        # Fetches a list of Books, skipping and limiting as specified
        books_cursor = collection.find().skip(skip).limit(limit)
        books = list(books_cursor)
        return books


    def get_with_author(self, collection: Collection) -> List[dict]:
        pipeline = [
            {
                "$lookup": {
                    "from": "author", 
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
        books = list(collection.aggregate(pipeline))
        for book in books:
            # MongoDB typically uses '_id' as the key for the object ID,
            # so we'll mimic the SQLAlchemy code and use 'id' instead.
            book['id'] = book.pop('_id')
            # Also, if necessary, convert '_id' from 'author_id' to string:
            if isinstance(book['author_id'], ObjectId):
                book['author_id'] = str(book['author_id'])
        return books

    
    def get_books_with_id(self, db: Collection, book_id: int) -> Dict[str, Any]:
        pipeline = [
            {
                "$match": {"_id": book_id}
            },
            {
                "$lookup": {
                    "from": "authors",  # Assuming the collection name for authors is 'authors'
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_info"
                }
            },
            {
                "$unwind": "$author_info"  # Unwind the resulting list of authors to emulate a JOIN
            },
            {
                "$project": {
                    "id": "$_id",
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"
                }
            }
        ]

        book_document = db.aggregate(pipeline).next()  # Use .next() to get the first match
        return book_document


    def update(
        self, collection: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict, Dict[str, Any]]
    ) -> Dict:
        # Check if obj_in is a dictionary. In SQLAlchemy, it's another model instance that's converted to a dict.
        # For PyMongo, we should receive already a dictionary
        if not isinstance(obj_in, dict):
            raise ValueError("obj_in must be a dictionary type")

        # MongoDB update method with $set
        result = collection.update_one({'_id': db_obj_id}, {'$set': obj_in})

        # Check if the update was successful
        if result.matched_count == 0:
            raise ValueError(f"No document found with id: {db_obj_id}")

        # MongoDB does not return the updated document by default.
        # Retrieve the updated document.
        updated_document = collection.find_one({'_id': db_obj_id})

        return updated_document


book_plain = CRUDBook()
