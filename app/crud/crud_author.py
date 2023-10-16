from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.json_util import dumps
from bson.objectid import ObjectId
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: str, *, obj_in: AuthorCreate) -> Author:
        client = MongoClient()
        database = client[db]
        collection = database['author']
        obj_in_data = loads(dumps(obj_in.dict()))
        result = collection.insert_one(obj_in_data)
        return result.inserted_id


    def get_all(self, db: MongoClient, collection: str, *, skip: int = 0, limit: int = 100) -> List[Dict[str,Any]]:
        cursor = db[collection].find().skip(skip).limit(limit)
        result = [jsonable_encoder(doc) for doc in cursor]
        return result


    def get(self, db: MongoClient, id: str):
        return db['authors'].find_one({"_id": ObjectId(id)})

    def update(self, db: str, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        client = MongoClient()
        database = client[db]
        collection = database['author']

        updated_object = collection.find_one_and_update(
            {"_id": db_obj['_id']},
            {"$set": obj_in}
        )

        return updated_object

author = CRUDAuthor(Author)
