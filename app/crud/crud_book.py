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
from typing import List, Dict
from typing import List
from pymongo.database import Database
from bson import ObjectId
from copy import deepcopy

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, collection: Collection, *, obj_in: BookCreate) -> dict:
        book_data = obj_in.dict()
        book_data['created_at'] = date.today()
        result = collection.insert_one(book_data)
        # When a document is inserted, a special key "_id" is automatically added if the document doesn’t already contain an "_id" key.
        new_book = collection.find_one({"_id": result.inserted_id})
        return new_book

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        cursor = collection.find().skip(skip).limit(limit)
        books = list(cursor)
        return books

    def get_with_author(self, db: Collection) -> List[dict]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'author',  # Assuming the author collection is named 'author'
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': '$author_info'
            },
            {
                '$project': {
                    '_id': False,
                    'id': '$_id',
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ]
        books_with_authors = list(db.aggregate(pipeline))
        return books_with_authors


    def get_books_with_id(self, db: Database, book_id: int):
        # Assuming that the 'books' collection contains a reference to 'authors' through 'author_id' field
        pipeline = [
            {
                "$match": {"_id": ObjectId(str(book_id))}
            },
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
                    "id": "$_id",
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"
                }
            }
        ]
        result = db.books.aggregate(pipeline)
        return result.next() if result.alive else None

    def update(self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], 'Book']) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # The comment about jsonable_encoder hints that we would encode the object for JSON,
            # but since we're working directly with Pymongo and BSON, let's assume 'obj_in' is a dictionary compatible with pymongo.
            # In production, you would likely need to convert your 'Book' object to a BSON-compatible dict.
            update_data = obj_in.to_mongo()  # This is a placeholder; actual implementation depends on 'Book' class specifics.

        updated_fields = {"$set": update_data}
        db_obj = db.find_one_and_update(
            {"_id": db_obj_id},
            updated_fields,
            return_document=True
        )
        
        return db_obj


book = CRUDBook(Book)
