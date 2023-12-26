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
from typing import Dict, Any, Union

ModelType = TypeVar("ModelType", bound=Base)
































































class CRUDBook(CRUDBase[Book, BookCreate, None]):

    def create(self, db: Collection, *, obj_in: BookCreate) -> dict:
        book_data = obj_in.dict()  # Convert Pydantic model to dictionary
        book_data['created_at'] = date.today()  # Set creation date

        # If author_id is expected to be an ObjectId in MongoDB
        if 'author_id' in book_data and isinstance(book_data['author_id'], str):
            book_data['author_id'] = ObjectId(book_data['author_id'])

        result = db.insert_one(book_data)  # Insert the book into the collection
        created_book = db.find_one({"_id": result.inserted_id})  # Retrieve the new book
        return created_book


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))

    
    def get_with_author(self, db: Collection) -> List[dict]:
        # Assuming 'db' is the books collection and it references authors through an 'author_id'
        # We perform an aggregation to lookup (join) authors on their '_id'
        books_with_authors = db.aggregate([
            {
                '$lookup': {
                    'from': 'authors',  # Assuming the authors collection is named 'authors'
                    'localField': 'author_id',  # The field in the books collection
                    'foreignField': '_id',  # The corresponding field in the authors collection
                    'as': 'author'  # The result will be an array with a single author document
                }
            },
            # Unwinds the 'author' array to make manipulation easier (converts array to a single item)
            {
                '$unwind': '$author'
            },
            # We can now project the fields we want to include in our response.
            {
                '$project': {
                    'id': '$_id',  # Assuming the books collection has an '_id' field
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,  # If you want to include the author_id in the result
                    'author_name': '$author.name'  # Gets the author's name
                }
            }
        ])
        
        return list(books_with_authors)

    
    def get_books_with_id(self, db: Collection, book_id: int):
        pipeline = [
            {
                '$match': {'_id': ObjectId(str(book_id))}
            },
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
                    '_id': 1,
                    'title': 1,
                    'pages': 1,
                    'created_at': 1,
                    'author_id': 1,
                    'author_name': '$author_info.name'
                }
            }
        ]
        
        book = db.aggregate(pipeline).next()
        return book

    def update(self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict, Dict[str, Any]]) -> Dict:
        updated_object = {}
        if isinstance(obj_in, dict):
            updated_object = {k: v for k, v in obj_in.items() if v is not None}

        db.update_one({'_id': db_obj_id}, {'$set': updated_object})

        return db.find_one({'_id': db_obj_id})


book = CRUDBook(Book)
