from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo import MongoClient
from typing import List
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
from typing import Any, Dict, Union
































class CRUDAuthor:

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict[str, Any]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = db.Author.insert_one(obj_in_data)
        return db_obj.inserted_id


    def get_all(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Author]:
        return list(db.author.find().skip(skip).limit(limit))


    def get(self, db, id: str):
        return db.authors.find_one({"_id": ObjectId(id)})


    def update(self, db: MongoClient, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        collection = db["authors"]
        obj_data = loads(dumps(db_obj))

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_dict = {}
        for field in obj_data:
            if field in update_data:
                update_dict[field] = update_data[field]

        collection.update_one({'_id': obj_data['_id']}, {"$set": update_dict})
        
        return collection.find_one({'_id': obj_data['_id']})


author_plain = CRUDAuthor()
