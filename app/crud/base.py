from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from bson.json_util import dumps, loads
from pymongo import MongoClient
from pymongo.database import Database
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import ObjectId

# database configuration
DATABASE = MongoClient()['CRUDBaseDB']
COLLECTION = DATABASE['CrudBaseCollection']

T = TypeVar("T", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, db: Database, collection: str):
        self.db = db
        self.collection = db[collection]

    def get(self, db: MongoClient, id: Any) -> Optional[ModelType]:        
        return db[self.model].find_one({"_id": ObjectId(id)})

    def get_multi(
        self, db: MongoClient, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return list(db[self.model].find().skip(skip).limit(limit))


    def create(self, db: MongoClient, *, obj_in: Dict, created_by=None) -> Dict:
        obj_in_data = dumps(obj_in)
        obj_in_data["created_by"] = created_by
        result = db.insert_one(obj_in_data)
        return result.inserted_id


    def update(
        self,
        db: MongoClient,
        *,
        collection_name: str,
        obj_id: str,
        obj_in: Union[BaseModel, Dict[str, Any]],
        modified_by= None
    ) -> Dict:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = jsonable_encoder(obj_in)
        update_data["modified_by"] = modified_by
        update_result = db[collection_name].update_one({'_id': obj_id}, {'$set': update_data})
        if update_result.matched_count > 0:
            return db[collection_name].find_one({"_id": obj_id})
        else:
            raise ValueError('No document found with provided id')


    @classmethod
    def remove(cls, *, id: int) -> Type[ModelType]:
        obj = COLLECTION.find_one({"_id": ObjectId(id)})
        COLLECTION.delete_one({"_id": ObjectId(id)})
        return obj
