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
from typing import List
from typing import Dict, Any

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: Collection, *, obj_in: BookCreate) -> dict:
        book_data = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": ObjectId(obj_in.author_id),
            "created_at": date.today()
        }
        # Insert the new book into the database
        result = db.insert_one(book_data)

        # Fetch the new book document using the inserted_id
        new_book = db.find_one({"_id": result.inserted_id})

        return new_book

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        books_cursor = collection.find().skip(skip).limit(limit)
        return list(books_cursor)

    def get_with_author(self, db: Collection) -> List[dict]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'author', 
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
                    'id': '$_id',
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author.name'
                }
            }
        ]
        return list(db.aggregate(pipeline))


    def get_books_with_id(self, db: Collection, book_id: int):
        # For the sake of example, assuming 'books_collection' and 'authors_collection'
        # are two Collection instances from pymongo representing 'books' and 'authors'
        # and also assuming MongoDB Atlas Search or $lookup is enabled in the MongoDB
        # instance to perform the join operation.

        # Convert book_id to ObjectId
        book_object_id = ObjectId(str(book_id))

        # MongoDB aggregation framework to perform the join and select specific fields
        aggregation_pipeline = [
            {
                '$match': {'_id': book_object_id}
            },
            {
                '$lookup': {
                    'from': 'authors',
                    'localField': 'author_id',
                    'foreignField': '_id',
                    'as': 'author_info'
                }
            },
            {
                '$unwind': '$author_info'  # Assuming there is always one author per book
            },
            {
                '$project': {
                    '_id': 1,
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ]

        return list(db.aggregate(aggregation_pipeline))


    def update(
        self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], 'Book']
    ) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        result = db.find_one_and_update(
            {"_id": db_obj_id},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            return result
        else:
            raise ValueError(f"No document found with id: {db_obj_id}")


book_plain = CRUDBook()
