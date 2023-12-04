from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from typing import Any, Optional
from pymongo.database import Database 
from pymongo.collection import Collection
from pymongo import MongoClient
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    def get_by_id(self, db: Database, collection: str, id: Any) -> Optional[dict]:
        result = db[collection].find_one({"_id": id})
        return result


    def get(
        self, db: Database, collection_name: str, *, skip: int = 0, limit: int = 100) -> Collection:
        return db[collection_name].find().skip(skip).limit(limit)

    def create(self, db: Database, collection: str, *, obj_in: Dict[str, Any], created_by=None) -> Dict[str, Any]:
        if created_by:
            obj_in["created_by"] = created_by
        result = db[collection].insert_one(obj_in)
        return result.inserted_id


    def update(
        self,
        db: Database,
        *,
        collection: str,
        filter: Dict[str, Any],
        obj_in: Union[Dict[str, Any], Dict[str, Any]],
        modified_by= None
    ):
        obj_data = db[collection].find_one(filter)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["modified_by"] = modified_by
        for field in obj_data:
            if field in update_data:
                db[collection].update_one({'_id': obj_data['_id']}, {'$set': {field: update_data[field]}})
      
        return db[collection].find_one(filter)


    def remove(self, db: Database, *, id: int) -> Dict[str, Any]:
        collection = db[self.model]
        obj = collection.find_one({"_id": id})
        collection.delete_one({"_id": id})
        return obj
