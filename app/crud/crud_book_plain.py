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
from pymongo.database import Database
from bson import ObjectId
from typing import List, Dict
from typing import List
from typing import Union, Dict, Any

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: Database, *, obj_in: dict) -> dict:
        collection: Collection = db.books
        db_obj = {
            "title": obj_in["title"],
            "pages": obj_in["pages"],
            "author_id": ObjectId(obj_in["author_id"]),  # Assuming author_id is stored as an ObjectId in MongoDB
            "created_at": date.today()
        }
        result = collection.insert_one(db_obj)
        new_book = collection.find_one({"_id": result.inserted_id})
        return new_book

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        books = collection.find({}).skip(skip).limit(limit)
        return list(books)


    def get_with_author(self, db: Database) -> List[Dict]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'author',
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
                    'id': 1,
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ]
        books_with_authors = list(db.get_collection("book").aggregate(pipeline))
        
        # Convert '_id' to 'id' and 'author_id' to the actual ObjectId string
        for book in books_with_authors:
            book['id'] = str(book.pop('_id'))
            if 'author_id' in book:
                book['author_id'] = str(book['author_id'])
        
        return books_with_authors

    def get_books_with_id(self, db: Database, book_id: int):
        # Assuming that the 'books' collection has references to authors by an 'author_id' field
        books_collection: Collection = db.get_collection('books')
        authors_collection: Collection = db.get_collection('authors')

        # Assuming that book_id is stored as an integer in the database
        book_data = books_collection.find_one({'_id': book_id}, {'_id': 0, 'author_id': 1, 'title': 1, 'pages': 1, 'created_at': 1})
        if not book_data:
            return None

        # Lookup the author's name using the author_id found in the book_data
        author_data = authors_collection.find_one({'_id': book_data['author_id']}, {'name': 1})
        if author_data:
            book_data['author_name'] = author_data.get('name', None)

        return book_data

    
    def update(
        self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict, Dict[str, Any]]
    ) -> Dict:
        # Find the document to be updated
        db_obj = db.find_one({"_id": db_obj_id})
        if db_obj is None:
            return {}  # Returning an empty dictionary to indicate no object was found to update

        # Prepare the update document
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        # Perform the update operation
        result = db.find_one_and_update(
            {"_id": db_obj_id},
            {"$set": update_data},
            return_document=True
        )
        
        return result


book_plain = CRUDBook()
