from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo import MongoClient
from bson import json_util
from typing import List
from bson.objectid import ObjectId
from typing import Any, Dict, Union
































class CRUDAuthor:

    def create(self, db: MongoClient, *, obj_in: AuthorCreate):
        obj_in_data = json_util.dumps(obj_in)
        result = db.authors.insert_one(obj_in_data)
        return result.inserted_id


    def get_all(self, skip: int = 0, limit: int = 100) -> List[dict]:
        client = MongoClient('localhost', 27017)
        mydb = client['mydb']
        authors = mydb['authors']
        return list(authors.find().skip(skip).limit(limit))


    def get(self, db, id: int):
        return db['author'].find_one({"_id": ObjectId(id)})


    def update(self, db, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in

        for field in db_obj:
            if field in update_data:
                db_obj[field] = update_data[field]

        db["authors"].update_one({"_id": db_obj["_id"]}, {"$set": db_obj})
        return db_obj


author_plain = CRUDAuthor()
