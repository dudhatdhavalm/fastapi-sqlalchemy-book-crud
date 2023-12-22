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

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: Collection, *, obj_in: dict) -> dict:
        obj_in_data = obj_in.dict(by_alias=True)
        obj_in_data['created_at'] = datetime.utcnow()
        result = db.insert_one(obj_in_data)
        created_book = db.find_one({"_id": result.inserted_id})
        return created_book

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        cursor = collection.find().skip(skip).limit(limit)
        return list(cursor)


    def get_with_author(self, db: Collection) -> List[Dict]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'authors',  # Assuming the authors collection name is 'authors'
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': {
                    'path': '$author_info',
                    # Preserve books without authors
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': 0,
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

    def get_books_with_id(self, db: Collection, book_id: Union[int, str, ObjectId]):
        # Convert the book_id to ObjectId if it's not already one
        if not isinstance(book_id, ObjectId):
            try:
                book_id = ObjectId(book_id)
            except Exception as e:
                print(f"Invalid ObjectId: {e}")
                return None

        # First, find the book by ID
        book = db.find_one({'_id': book_id})

        if not book:
            return None

        # Now let's assume that the 'authors' collection exists and
        # that each book document contains an 'author_id' field which is a reference to an author document
        authors_collection = db.database.get_collection('authors')
        
        # Assuming that 'author_id' in book refers to '_id' in the authors collection
        author_id = book.get('author_id')
        if isinstance(author_id, ObjectId):
            # Find the author by ID
            author = authors_collection.find_one({'_id': author_id})
            if author:
                # Include author_name in the result
                book['author_name'] = author.get('name', 'Unknown')
        
        return book

    def update(
        self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[dict, Dict[str, Any]]
    ) -> dict:
        if isinstance(db_obj_id, ObjectId):
            filter_query = {"_id": db_obj_id}
        else:
            raise ValueError("db_obj_id must be an instance of ObjectId.")

        if isinstance(obj_in, dict):
            update_data = {'$set': obj_in}
        else:
            raise ValueError("obj_in must be a dictionary.")

        update_result = db.update_one(filter_query, update_data)

        if update_result.matched_count:
            updated_document = db.find_one(filter_query)
            return updated_document
        else:
            raise ValueError("No document found with the provided ObjectId.")


book_plain = CRUDBook()
