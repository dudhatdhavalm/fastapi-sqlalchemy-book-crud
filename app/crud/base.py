from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pymongo.collection import Collection
from typing import TypeVar, Generic
from typing import Any, Optional, TypeVar, Generic
from typing import Any, TypeVar, Generic
from typing import Any, Dict, Union

# Assuming CreateSchemaType is a subclass of BaseModel with the required fields for creating
# a document in a MongoDB collection.
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

# ModelType represents a dummy class to satisfy the TypeVar used in the method signature
# since pymongo works directly with dictionaries, there's no model class.
ModelType = TypeVar("ModelType", bound=dict)

# Define a type variable that can be any type.
ModelType = TypeVar('ModelType')

# Type variable for the type of the document
DocumentType = TypeVar('DocumentType', bound=dict)
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, collection: Collection):
        self.collection = collection

    # Define a method to get an object by id using PyMongo.
    def get_by_id(self, collection: Collection, id: Any) -> Optional[ModelType]:
        return collection.find_one({'_id': id})

    
    def get(
        self, db: Collection, *, skip: int = 0, limit: int = 100
    ) -> List[dict]:
        # Retrieve documents from a MongoDB collection, limited and offset.
        return list(db.find().skip(skip).limit(limit))

    
    def create(self, db: Collection, *, obj_in: CreateSchemaType, created_by=None) -> ModelType:
        obj_in_data = obj_in.dict()  # Converting Pydantic object to dictionary
        if created_by:
            obj_in_data["created_by"] = created_by
        inserted_id = db.insert_one(obj_in_data).inserted_id
        # pymongo doesn't return the whole document by default on inserting, so we need to retrieve it
        db_obj = db.find_one({"_id": inserted_id})
        return db_obj

    def update(
        self,
        collection: Collection,
        *,
        filter_query: Dict[str, Any],
        update_data: Union[Dict[str, Any]],
        modified_by: Optional[Any] = None
    ) -> Any:
        if 'modified_by' not in update_data:
            update_data['modified_by'] = modified_by
        updated_result = collection.find_one_and_update(
            filter_query,
            {'$set': update_data},
            return_document=True
        )
        return updated_result

    def remove(self, collection: Collection, *, id: Any) -> dict:
        # In pymongo, you would typically use the ObjectId for the '_id' field but here we'll allow any id type
        obj = collection.find_one({'_id': id})
        if obj:
            collection.delete_one({'_id': id})
        return obj
