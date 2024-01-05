from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from typing import TypeVar, Generic, Type
from pymongo.collection import Collection
from typing import Any, Optional
from typing import List, TypeVar, Type, Generic
from bson import ObjectId
from typing import Any, Dict, Union

# Type variables to use for the CreateSchemaType and ModelType
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
ModelType = TypeVar('ModelType', bound=dict)

# A generic type variable that can be any type
ModelType = TypeVar("ModelType")

# Assuming BaseModel is a Pydantic model here, which is common with FastAPI
ModelType = TypeVar('ModelType', bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):


    def __init__(self, collection: Collection, model: Type[ModelType]):
        self.collection = collection
        self.model = model

    def get_by_id(self, collection: Collection, id: Any) -> Optional[dict]:
        return collection.find_one({'_id': id})


    def get(
        self, db: Collection, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return list(db.find().skip(skip).limit(limit))


    def create(self, collection: Collection, *, obj_in: CreateSchemaType, created_by=None) -> ModelType:
        obj_in_data = obj_in.dict()  # Convert the Pydantic model to a dictionary
        obj_in_data["created_by"] = created_by
        result = collection.insert_one(obj_in_data)  # Insert the document into the collection

        # In MongoDB, the inserted ID is returned in the result, so we use it to retrieve the created object
        created_obj = collection.find_one({"_id": result.inserted_id})

        # Assuming created_obj is a dictionary that represents the created document
        return created_obj

    def update(
        self,
        collection: Collection,
        *,
        db_obj_id: ObjectId,
        obj_in: Union[Dict[str, Any], None],
        modified_by=None
    ) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if modified_by is not None:
            update_data["modified_by"] = modified_by

        update_result = collection.update_one({"_id": db_obj_id}, {"$set": update_data})
        
        if update_result.modified_count:
            return collection.find_one({"_id": db_obj_id})
        else:
            return None


    def remove(self, db: Collection, *, id: ObjectId) -> dict:
        obj = db.find_one({"_id": id})
        if obj:
            db.delete_one({"_id": id})
        return obj
