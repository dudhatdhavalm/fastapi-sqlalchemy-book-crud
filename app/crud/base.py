from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pymongo.collection import Collection
from typing import TypeVar, Generic
from typing import Any, Optional, TypeVar, Generic
from typing import List, Dict
from typing import Any, Dict
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Any, Dict, Union

# Define a type variable that can be used to denote the model class
ModelType = TypeVar('ModelType')

# Type variable to represent any pydantic model instance
ModelType = TypeVar('ModelType', bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, collection: Collection):
        self.collection = collection


    def get_by_id(self, db: Collection, id: Any) -> Optional[ModelType]:
        return db.find_one({'_id': id})

    # Example method (You can create actual methods as per your requirements)
    def find_one(self, filter_: dict) -> Optional[ModelType]:
        document = self.collection.find_one(filter_)
        return document if document else None


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        return list(db.find().skip(skip).limit(limit))

    def create(self, collection: Collection, *, obj_in: Dict[Any, Any], created_by=None) -> Dict:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["created_by"] = created_by
        inserted_result = collection.insert_one(obj_in_data)
        created_obj = collection.find_one({"_id": inserted_result.inserted_id})
        return created_obj

    def update(
        self,
        collection: Collection,
        *,
        filter_data: Dict[str, Any],
        update_data: Union[Dict[str, Any], Any],
        modified_by=None
    ) -> Dict[str, Any]:
        if isinstance(update_data, dict):
            update_data = {"$set": update_data}
        else:
            update_data = {"$set": update_data.dict(exclude_unset=True)}
        
        if modified_by is not None:
            update_data["$set"]["modified_by"] = modified_by

        updated_document = collection.find_one_and_update(
            filter_data,
            update_data,
            return_document=ReturnDocument.AFTER
        )
        
        return updated_document

    def remove(self, db: Collection, *, id: Any) -> Dict:
        # In pymongo, we need to convert the id to ObjectId if it's a string
        if isinstance(id, str):
            id = ObjectId(id)
        result = db.find_one_and_delete({"_id": id})

        return result
