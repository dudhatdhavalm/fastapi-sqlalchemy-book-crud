from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.json_util import dumps, loads
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def get(self, db: Collection, id: Any) -> Optional[ModelType]:        
        return db.find_one({"_id": ObjectId(id)})

    def get_multi(
        self, db: MongoClient, *, skip: int = 0, limit: int = 100
    ) -> List:
        return db.find().skip(skip).limit(limit)

    def create(self, *, obj_in: Dict, created_by=None) -> Dict:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        collection = db[self.model]
        obj_in["created_by"] = created_by
        db_obj = collection.insert_one(obj_in)
        return loads(dumps(db_obj.inserted_id))


    def update(
        self,
        db_collection,
        *,
        db_obj: Dict[str, Any],
        obj_in: Union[Dict[str, Any], Dict[str, Any]],
        modified_by = None
    ) -> Dict[str, Any]:

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["modified_by"] = modified_by

        update_db = {'$set': update_data}
        db_collection.update_one(db_obj, update_db)

        db_obj = db_collection.find_one(db_obj)
        
        return db_obj


    def remove(self, db, *, id: int):
        obj = db.find_one({"_id": ObjectId(id)})
        db.delete_one({"_id": ObjectId(id)})
        return obj
