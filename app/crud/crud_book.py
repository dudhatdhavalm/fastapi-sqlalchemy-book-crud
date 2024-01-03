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
from pymongo.database import Database
from typing import List, Dict
from typing import Any, Dict

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db: Collection, *, obj_in: dict) -> dict:
        obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        obj_in_data['created_at'] = date.today().isoformat()
        result = db.insert_one(obj_in_data)
        new_book = db.find_one({'_id': result.inserted_id})
        return new_book

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        Get a list of books from the MongoDB collection.

        :param collection: The pymongo collection object where the books are stored
        :param skip: Number of records to skip for pagination
        :param limit: Max number of records to return
        :return: A list of book documents
        """
        return list(collection.find().skip(skip).limit(limit))

    def get_with_author(self, db: Database) -> List[Dict]:
        # Here the assumption is that the 'books' collection is embedded with author information
        # Adjust the projection fields accordingly based on your MongoDB schema
        books_with_authors = db.books.aggregate([
            # Lookup (join) with the 'authors' collection
            {
                "$lookup": {
                    "from": "authors",  # This should be the name of your authors collection
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_info"
                }
            },
            # Project the fields you want to include in the result
            {
                "$project": {
                    "id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"  # Assumes author's name is stored in 'name' field
                }
            },
            # Deconstruct the author_info array to get the first element (should only be one)
            {
                "$unwind": {
                    "path": "$author_info",
                    "preserveNullAndEmptyArrays": True  # To keep books without authors
                }
            },
            # Amend the projection to correct author_name field after the unwind
            {
                "$project": {
                    "id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": "$author_info.name"  # Assuming the author's name is stored in 'name'
                }
            }
        ])
        return list(books_with_authors)

    def get_books_with_id(self, db: Database, book_id: str):
        # Assuming 'books' collection contains the books and each book document
        # has an 'author_id' field which is a reference to a document in the 'authors' collection.
        # Also, the ObjectIds are used to uniquely identify documents.

        # We need to convert book_id to ObjectId if it's a valid ObjectId string
        if ObjectId.is_valid(book_id):
            book_object_id = ObjectId(book_id)
        else:
            return None  # or handle invalid book_id appropriately

        # Perform an aggregation to get the book with the corresponding author name
        pipeline = [
            {'$match': {'_id': book_object_id}},
            {'$lookup': {
                'from': 'authors',
                'localField': 'author_id',
                'foreignField': '_id',
                'as': 'author_info'
            }},
            {'$unwind': '$author_info'},  # Assuming each book has only one author
            {'$project': {
                '_id': 1,
                'title': 1,
                'pages': 1,
                'created_at': 1,
                'author_id': 1,
                'author_name': '$author_info.name'
            }}
        ]

        book = db['books'].aggregate(pipeline).next()

        return book


    def update(self, db: Collection, *, obj_id: ObjectId, obj_in: Dict[str, Any]) -> Dict:
        if isinstance(obj_in, dict):
            update_data = {k: v for k, v in obj_in.items() if not k.startswith("_")}
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        result = db.find_one_and_update(
            {"_id": obj_id},
            {"$set": update_data},
            return_document=True  # This will return the updated document
        )
        return result


book = CRUDBook(Book)
