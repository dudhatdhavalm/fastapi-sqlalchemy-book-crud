from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo import MongoClient
from bson import ObjectId
from typing import Any, Dict, Union
































class CRUDAuthor:

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict:
        obj_in_data = obj_in.dict()
        db_obj = db['Author'].insert_one(obj_in_data)
        inserted_id = db_obj.inserted_id
        return db['Author'].find_one({"_id": ObjectId(inserted_id)})


    def get(self, db: MongoClient, collection: str, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db[collection].find().skip(skip).limit(limit))


    def get_by_author_id(self, db: MongoClient, id: Union[str, ObjectId]):
        return db['author'].find_one({"_id": ObjectId(id)})


    def update(self, db: MongoClient, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any]]) -> Dict:
        obj_data = db['authors'].find_one({"_id": db_obj_id})
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                obj_data[field] = update_data[field]

        db['authors'].update_one({"_id": db_obj_id}, {"$set": obj_data})
        return obj_data


author_plain = CRUDAuthor()
