from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from bson.json_util import dumps
from typing import Any, Dict, Union

client = MongoClient('localhost', 27017)
db = client['mydatabase']
author_collection = db['author']

class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = db.authors.insert_one(obj_in_data)
        return db.authors.find_one({'_id': ObjectId(db_obj.inserted_id)})


    def get_all(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db["Author"].find().skip(skip).limit(limit))


    def get(self, db: str, id: int):
        client = MongoClient()
        db = client[db]
        author_collection = db['author']
        return author_collection.find_one({"_id": id})


    def update(self, *, db_obj_id: str, obj_in: Union[Dict[str, Any]]) -> Dict[str, Any]:
        obj_in_data = jsonable_encoder(obj_in)
        db.author_collection.update_one({'_id': ObjectId(db_obj_id)}, {"$set": obj_in_data} )
        return db.author_collection.find_one({'_id': ObjectId(db_obj_id)})

author = CRUDAuthor(Author)
