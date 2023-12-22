from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo.collection import Collection
from bson import ObjectId
from typing import List
from typing import Dict, Any
































class CRUDAuthor:

    def create(self, collection: Collection, *, obj_in: AuthorCreate) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.dict(by_alias=True)

        result = collection.insert_one(obj_in_data)
        new_author = collection.find_one({"_id": result.inserted_id})
        return new_author


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        authors_cursor = db.find().skip(skip).limit(limit)
        return list(authors_cursor)


    def get_by_author_id(self, collection: Collection, id: int):
        return collection.find_one({"_id": ObjectId(str(id))})

    
    def update(self, db: Collection, *, db_obj: Dict[str, Any], obj_in: Dict[str, Any]) -> Dict[str, Any]:
        if "_id" in db_obj:
            # Create a copy of db_obj excluding '_id'
            obj_data = {k: v for k, v in db_obj.items() if k != "_id"}

            # If obj_in is a dictionary, use it as update_data
            update_data = obj_in

            # Update statement
            db.update_one({"_id": db_obj["_id"]}, {"$set": update_data})
            
            # Get the updated document
            updated_document = db.find_one({"_id": db_obj["_id"]})
            
            return updated_document
        else:
            raise ValueError("The provided db_obj does not contain a valid '_id'.")


author_plain = CRUDAuthor()
