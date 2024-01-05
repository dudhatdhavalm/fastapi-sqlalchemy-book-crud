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
from typing import List
from typing import List, Dict
from bson.objectid import ObjectId
from typing import Any, Dict, Union

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook:

    def create(self, db: Database, *, obj_in: BookCreate) -> dict:
        collection: Collection = db.get_collection('books')

        db_obj = {
            "title": obj_in.title, 
            "pages": obj_in.pages, 
            "author_id": obj_in.author_id,
            "created_at": date.today()
        }

        result = collection.insert_one(db_obj)
        new_book = collection.find_one({"_id": result.inserted_id})
        return new_book


    def get(self, db: Database, *, skip: int = 0, limit: int = 100) -> List[Book]:
        book_collection: Collection = db.get_collection('book_collection_name') # Replace 'book_collection_name' with your actual collection name
        books_cursor = book_collection.find().skip(skip).limit(limit)
        books: List[Book] = list(books_cursor)
        return books

    def get_with_author(self, db: Database) -> List[Dict]:
        books_with_authors = db.books.aggregate([
            {
                '$lookup': {
                    'from': 'authors',
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
                    '_id': 0,
                    'id': '$_id',
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ])
        return list(books_with_authors)

    def get_books_with_id(self, db: Database, book_id: int):
        books_collection = db.get_collection('books')
        authors_collection = db.get_collection('authors')
        
        # Assuming there is a reference from the books collection to the authors collection via 'author_id'
        book = books_collection.find_one({"_id": ObjectId(book_id)})
        if book:
            author = authors_collection.find_one({"_id": book["author_id"]})
            if author:
                book["author_name"] = author["name"]
        return book


    def update(
        self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if isinstance(db_obj_id, ObjectId):
            update_data = {"$set": obj_in}
        else:
            raise ValueError("The db_obj_id must be an instance of ObjectId.")
        
        result = db.update_one({"_id": db_obj_id}, update_data)
        
        if result.modified_count:
            updated_document = db.find_one({"_id": db_obj_id})
            return updated_document
        else:
            raise ValueError("No document was updated, check your db_obj_id or obj_in.")


book_plain = CRUDBook()
