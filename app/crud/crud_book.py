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
from typing import List
from bson.objectid import ObjectId
from app.models.book import Book  # Assuming there is a Book model class that can be used
from typing import List, Dict
from pymongo.database import Database
from typing import Dict, Any, Union

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db: Collection, *, obj_in: BookCreate) -> dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": obj_in.author_id,
            "created_at": date.today()
        }
        # In pymongo, db represents the collection
        insert_result = db.insert_one(db_obj)
        # Retrieving complete inserted document
        new_book = db.find_one({"_id": insert_result.inserted_id})
        return new_book

    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Book]:
        books_cursor = db.find().skip(skip).limit(limit)
        return [Book(**book) for book in books_cursor]

    def get_with_author(self, collection: Collection) -> List[Dict]:
        # Assuming 'books' is the primary collection and it contains an 'author_id' field.
        # Also assuming there is another collection 'authors' that contains an 'id' field.
        pipeline = [
            {
                "$lookup": {
                    "from": "authors",      # replace with the name of your authors collection
                    "localField": "author_id",
                    "foreignField": "_id",  # replace with the actual field name in authors collection if different
                    "as": "author_info"
                }
            },
            {
                "$unwind": "$author_info"  # Unwinds the resulting array from lookup
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"  # replace 'name' with the actual name field in authors collection
                }
            }
        ]
        books_with_authors = list(collection.aggregate(pipeline))
        return books_with_authors


    def get_books_with_id(self, db: Database, book_id: ObjectId):
        book = db.books.aggregate([
            {
                '$match': {'_id': book_id}
            },
            {
                '$lookup': {
                    'from': 'authors',
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author'
                }
            },
            {
                '$unwind': '$author'
            },
            {
                '$project': {
                    '_id': 1,
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author.name'
                }
            },
            {
                '$limit': 1
            }
        ]).next()
        
        return book

    
    def update(self, db: Database, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], Book]) -> Dict[str, Any]:
        book_collection = db.get_collection("books")
        
        updated_data = {}
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)
        
        result = book_collection.update_one({"_id": db_obj_id}, {"$set": updated_data})
        if result.matched_count:
            return book_collection.find_one({"_id": db_obj_id})
        else:
            raise ValueError(f"No book found with id: {db_obj_id}")


book = CRUDBook(Book)
