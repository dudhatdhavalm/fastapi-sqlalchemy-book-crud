from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from typing import TypeVar, Generic, Type
from pymongo.collection import Collection
from typing import List, TypeVar, Generic, Type
from bson import ObjectId
from typing import Any, Dict, Union

ModelType = TypeVar('ModelType')

# Since the same TypeVar ModelType is not available in the scope,
# redefining ModelType here to be used in the CRUDBase class.
ModelType = TypeVar("ModelType")

# Generic Type for Documents
DocumentType = TypeVar('DocumentType', bound=dict)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, collection: Collection):
        self.collection = collection

    def get_by_id(self, collection: Collection, id: Any) -> Optional[Dict]:
        return collection.find_one({'_id': id})

    
    def get(
        self, collection: Collection, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return list(collection.find().skip(skip).limit(limit))

    def create(self, collection: Collection, *, obj_in: dict, created_by=None) -> dict:
        obj_in_data = jsonable_encoder(obj_in)
        if created_by is not None:
            obj_in_data["created_by"] = created_by
        result = collection.insert_one(obj_in_data)
        created_obj = collection.find_one({"_id": result.inserted_id})
        return created_obj


    def update(
        self,
        db_collection: Collection,
        *,
        db_obj_id: Union[str, ObjectId],
        obj_in: Union[Dict[str, Any], Dict[str, Any]],
        modified_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        if isinstance(db_obj_id, str):
            db_obj_id = ObjectId(db_obj_id)
        
        update_data = { "$set": obj_in }
        if modified_by is not None:
            update_data["$set"]["modified_by"] = modified_by
        
        result = db_collection.find_one_and_update(
            {"_id": db_obj_id},
            update_data,
            return_document=True
        )

        return result


    def remove(self, db: Collection, *, id: str) -> dict:
        result = db.find_one_and_delete({"_id": ObjectId(id)})
        return result
