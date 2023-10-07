from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from bson import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps, loads

class CRUDAuthor:

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict:
        obj_in_data = jsonable_encoder(obj_in)
        result = db.myDb.myCollection.insert_one(obj_in_data)
        return result.inserted_id


    def get_all(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(db.author.find().skip(skip).limit(limit))


    def get(self, db: MongoClient, id: int):
        # use the .find_one() method specifying the criterion as the 'id' field
        return db['Author'].find_one({"_id": ObjectId(id)})


    def update(self, db: MongoClient, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        obj_in_data = loads(dumps(obj_in))
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in db_obj.keys():
            if field in update_data:
                db_obj[field] = update_data[field]

        db.author.update_one({'_id': db_obj['_id']}, {"$set": db_obj}, upsert=True)

        return db_obj


author_plain = CRUDAuthor()
