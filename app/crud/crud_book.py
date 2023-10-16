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
from typing import Dict, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.database import Database
from typing import Any, Dict, List, Union
from bson import ObjectId
from datetime import datetime
import pymongo
from typing import Any, Dict, Union


client = MongoClient('localhost', 27017)
db = client['mydatabase']
books_collection = db['books']

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    @staticmethod
    def create(obj_in: Dict[str, Any]) -> Optional[Dict]:
        obj_in["created_at"] = date.today()
        result = books_collection.insert_one(obj_in)
        return books_collection.find_one({"_id": ObjectId(result.inserted_id)})

    def get_multi(self, db: Database, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        return list(db['book'].find().skip(skip).limit(limit))


    def get_with_author(self, client: MongoClient, books_collection: str = 'books', authors_collection: str = 'authors') -> List[Dict]:
        books = list(map(lambda doc: doc, client[books_collection].find({})))
        authors = list(map(lambda doc: doc, client[authors_collection].find({})))

        for book in books:
            for author in authors:
                if str(book.get('author_id')) == str(author.get('_id')):
                    book['author_name'] = author['name']
                    del book['author_id']

        return books

    
    def get_books_with_id(self, db: MongoClient, book_id: int):
        books = db.books.aggregate([
            {
                "$lookup":
                {
                    "from": "author",
                    "localField": "author_id",
                    "foreignField": "_id",
                    "as": "author_name"
                }
            },
            {
                "$match":
                {
                    "_id": ObjectId(book_id)
                }
            },
            {
                "$project":
                {
                    "_id": 1,
                    "title": 1,
                    "pages": 1,
                    "created_at": 1,
                    "author_id": 1,
                    "author_name": {"$arrayElemAt": ["$author_name.name", 0]}
                }
            }
        ]).next()
        
        return books


    def update(self, db: MongoClient, *, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]) -> Book:
        db_obj['created_at'] = date.today().isoformat()
        db['database_name']['collection_name'].update_one({"_id": db_obj["_id"]}, {"$set": db_obj})
        return db_obj


book = CRUDBook(Book)
