from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo.collection import Collection
from typing import List
from app.models.author import Author  # This import may need to be adjusted to fit your actual model path and structure.
from typing import Dict, Union
from bson import ObjectId
































class CRUDAuthor:

    def create(self, db: Collection, *, obj_in: AuthorCreate) -> Author:
        obj_in_data = obj_in.dict()
        db_obj = db.insert_one(obj_in_data)
        new_author = db.find_one({"_id": db_obj.inserted_id})
        return Author(**new_author)

    
    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Author]:
        authors_cursor = db.find().skip(skip).limit(limit)
        authors = [Author(**author) for author in authors_cursor]
        return authors


    def get_by_author_id(self, db: Database, id: int):
        # Assuming the MongoDB collection is named 'authors' and 'id' is the field we're querying by.
        # MongoDB typically uses '_id' for its primary key field, so you might have to adjust the query
        # if your schema uses '_id' or a different field for the author's ID.
        return db.authors.find_one({'id': id})


    def update(self, collection: Collection, *, db_obj_id: Union[str, ObjectId], obj_in: Union[Dict[str, Any]]) -> Dict:
        if isinstance(db_obj_id, str):
            db_obj_id = ObjectId(db_obj_id)

        update_data = {"$set": obj_in}
        collection.update_one({"_id": db_obj_id}, update_data)
        db_obj = collection.find_one({"_id": db_obj_id})
        return db_obj


author_plain = CRUDAuthor()
