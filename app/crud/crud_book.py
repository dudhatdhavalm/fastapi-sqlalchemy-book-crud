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
from typing import List
from bson.objectid import ObjectId
from bson import ObjectId

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db_collection: Collection, *, obj_in: BookCreate) -> dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            "author_id": obj_in.author_id,
            "created_at": datetime.today()
        }
        result = db_collection.insert_one(db_obj)
        # The inserted_id attribute contains the ID of the inserted document
        created_document = db_collection.find_one({"_id": result.inserted_id})
        return created_document

    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        return list(db.find().skip(skip).limit(limit))

    
    def get_with_author(self, db: Collection) -> List[dict]:
        pipeline = [
            {
                "$lookup": {
                    "from": "authors",  # the collection to join with
                    "localField": "author_id",  # the field from the books collection
                    "foreignField": "_id",  # the field from the authors collection
                    "as": "author_info"  # the output array field
                }
            },
            {
                "$unwind": "$author_info"  # deconstruct the array field to object
            },
            {
                "$project": {
                    "_id": 0,  # Assuming you don't want to include the _id in the results, if not just remove this line
                    "id": "$_id",
                    "title": 1,  # include the title field
                    "pages": 1,  # include the pages field
                    "created_at": 1,  # include the created_at field
                    "author_id": 1,  # include the author_id field
                    "author_name": "$author_info.name"  # include the author's name from the author_info
                }
            }
        ]

        return list(db.aggregate(pipeline))

    def get_books_with_id(self, collection: Collection, book_id: str):
        # Assuming book_id is a string representation of ObjectId
        try:
            object_id = ObjectId(book_id)
        except:
            return None  # or handle invalid ObjectId error
        
        # Assuming a single collection contains both books and authors,
        # and book documents have an 'author_id' field containing ObjectId reference to the author.
        pipeline = [
            {
                '$match': {'_id': object_id}
            },
            {
                '$lookup': {
                    'from': 'authors',  # This is the name of the authors collection
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
                    '_id': 1,
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ]
        
        return list(collection.aggregate(pipeline)).first()

    def update(self, collection: Collection, *, db_obj_id: ObjectId, obj_in: Union[dict, Book]) -> dict:
        if isinstance(obj_in, dict):
            update_data = {k: v for k, v in obj_in.items() if v is not None}
        else:
            update_data = obj_in.dict(exclude_unset=True)

        updated_result = collection.find_one_and_update(
            {"_id": db_obj_id},
            {"$set": update_data},
            return_document=True
        )
        return updated_result


book = CRUDBook(Book)
