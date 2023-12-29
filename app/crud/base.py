from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pymongo.collection import Collection
from typing import Dict, Any
from typing import Any, Optional
from typing import List
from bson import ObjectId
from typing import Any, Dict, Union, TypeVar
from typing import Dict, Union

# Considering that 'ModelType' and 'CreateSchemaType' TypeVars
# should be replaced with specific types or Pydantic models as required for your MongoDB data model.
ModelType = TypeVar('ModelType')
CreateSchemaType = TypeVar('CreateSchemaType')
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
































































































































class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, collection: Collection):
        self.collection = collection


    def get_by_id(self, db: Collection, id: Any) -> Optional[dict]:
        return db.find_one({"_id": id})


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))

    # No __init__ method according to the instructions
    
    def create(self, db: Collection, *, obj_in: CreateSchemaType, created_by: Optional[Any] = None) -> Dict[str, Any]:
        # In MongoDB, Python dictionaries are directly used to insert documents
        obj_in_data: Dict[str, Any] = jsonable_encoder(obj_in)
        if created_by:
            obj_in_data["created_by"] = created_by
        # Insert the document into the MongoDB collection
        result = db.insert_one(obj_in_data)
        # Retrieve the inserted document's ID
        document_id = result.inserted_id
        # Fetch the newly created document using the retrieved ID and return it
        created_document = db.find_one({"_id": document_id})
        # If needed, convert the ObjectId to a string
        if created_document and "_id" in created_document:
            created_document["_id"] = str(created_document["_id"])
        return created_document  # Contains the full document that was inserted

    def update(
        self,
        db: Collection,
        *,
        db_obj_id: Union[str, ObjectId],
        obj_in: Dict[str, Any],
        modified_by: Union[str, ObjectId] = None
    ) -> Dict:
        update_data = {'$set': obj_in}
        if modified_by is not None:
            update_data['$set']['modified_by'] = modified_by

        # Assuming the db_obj_id is passed as an ObjectId or string that needs conversion to ObjectId
        if isinstance(db_obj_id, str):
            filter_query = {'_id': ObjectId(db_obj_id)}
        else:
            filter_query = {'_id': db_obj_id}

        result = db.find_one_and_update(filter_query, update_data, return_document=True)
        return result

    def remove(self, collection: Collection, *, id: Union[str, ObjectId]) -> Dict:
        if isinstance(id, str):
            id = ObjectId(id)
        obj = collection.find_one({"_id": id})
        collection.delete_one({"_id": id})
        return obj
