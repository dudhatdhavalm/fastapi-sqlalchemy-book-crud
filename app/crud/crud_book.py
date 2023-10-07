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
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from typing import Any, Dict, Union
from datetime import datetime


client = MongoClient('mongodb://localhost:27017/')
db = client['YourDatabaseName']

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, *, obj_in: BookCreate) -> Dict:
        db_obj = {
            "title": obj_in.title,
            "pages": obj_in.pages,
            'author_id': obj_in.author_id,
            "created_at": date.today()
        }
        result = db['YourCollectionName'].insert_one(db_obj)
        return dumps(db['YourCollectionName'].find_one({'_id': result.inserted_id}))


    def get_multi(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Book]:
        return list(db.book_collection.find().skip(skip).limit(limit))


    def get_with_author(self, db: MongoClient) -> List[Dict]:
        books = db["books"].aggregate([
           {
               "$lookup": {
                   "from": "authors",
                   "localField": "author_id",
                   "foreignField": "_id",
                   "as": "author"
               }
           },
           {
               "$project": {
                   "_id": 0,
                   "id": "$_id",
                   "title": 1,
                   "pages": 1,
                   "created_at": 1,
                   "author_id": 1,
                   "author_name": {"$arrayElemAt": ["$author.name", 0]}
               }
           }
        ])
        return list(books)

    def get_books_with_id(self, db, book_id: int):
        # ObjectId is used in PyMongo to convert string id to MongoDB's ObjectId
        books = db.books.find_one(
            {"_id": ObjectId(book_id)},
            {"_id": 1, "title": 1, "pages": 1, "created_at": 1, "author_id": 1, "author_name": 1}
        )
        return books


    def update(self, db: MongoClient, *, db_obj: ObjectId, obj_in: Union[Dict, Dict[str, Any]]) -> Dict:
        db.books.update_one({'_id': db_obj}, 
                            {'$set': { 'created_at': datetime.now()}},
                            upsert=True)
        return db.books.find_one({'_id': db_obj})


book = CRUDBook(Book)
