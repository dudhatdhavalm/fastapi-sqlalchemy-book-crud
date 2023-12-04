from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import loads, dumps
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict:
        obj_in_data = loads(dumps(obj_in))
        result = db.authors.insert_one(obj_in_data)
        return db.authors.find_one({"_id": result.inserted_id})


    def get(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        collection = db['authors']
        authors = list(collection.find().skip(skip).limit(limit))
        return authors


    def get_by_author_id(self, db: MongoClient, id: Any) -> Dict:
        collection = db["author"]
        return loads(dumps(collection.find_one({"_id": ObjectId(id)})))


    def update(self, db: MongoClient, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        if isinstance(obj_in, str):
            update_data = loads(obj_in)
        else:
            update_data = obj_in

        db[db_obj['collection']].update_one(
            {"_id": ObjectId(db_obj["_id"])}, 
            {"$set": update_data}
        )

        updated_document = db[db_obj['collection']].find_one({"_id": ObjectId(db_obj["_id"])})
        
        return jsonable_encoder(updated_document)

author = CRUDAuthor(Author)
