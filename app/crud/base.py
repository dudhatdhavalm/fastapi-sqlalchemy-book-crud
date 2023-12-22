from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pymongo.collection import Collection
from typing import Any, Optional
from bson.objectid import ObjectId
from typing import List
from bson import ObjectId
from typing import Dict, Any, Union

ModelType = TypeVar("ModelType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, collection: Collection):
        self.collection = collection


    def get_by_id(self, collection: Collection, id: Any) -> Optional[dict]:
        if isinstance(id, str):
            # Assuming 'id' is a string representation of ObjectId
            try:
                # Convert to ObjectId
                id = ObjectId(id)
            except Exception:
                return None
        return collection.find_one({'_id': id})

    def get(
        self, collection: Collection, *, skip: int = 0, limit: int = 100
    ) -> List[dict]:
        return list(collection.find().skip(skip).limit(limit))

    
    def create(self, collection: Collection, *, obj_in: BaseModel, created_by=None):
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["created_by"] = created_by
        result = collection.insert_one(obj_in_data)
        created_obj = collection.find_one({"_id": result.inserted_id})
        return created_obj

    def update(
        self,
        db: Collection,
        *,
        db_obj_id: Union[str, ObjectId],
        obj_in: Union[Dict[str, Any], Any],
        modified_by=None
    ) -> Dict[str, Any]:
        # Convert string ID to ObjectId if necessary
        if isinstance(db_obj_id, str):
            db_obj_id = ObjectId(db_obj_id)

        # If obj_in is not a dictionary, it should have a method to convert it into one
        update_data = obj_in
        if not isinstance(obj_in, dict):
            update_data = obj_in.dict()

        # Include the modified_by field in the update
        update_data["modified_by"] = modified_by

        # Prepare the update document
        update_doc = {"$set": update_data}

        # Perform the update operation
        db.update_one({"_id": db_obj_id}, update_doc)

        # Retrieve the updated document
        updated_db_obj = db.find_one({"_id": db_obj_id})

        return updated_db_obj

    def remove(self, collection: Collection, *, id: Union[str, ObjectId]) -> dict:
        if isinstance(id, str):
            id = ObjectId(id)
        result = collection.find_one_and_delete({"_id": id})
        return result
