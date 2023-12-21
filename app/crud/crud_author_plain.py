from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo.collection import Collection
from bson import ObjectId
from typing import List
from typing import Any, Dict, Union
































class CRUDAuthor:

    def create(self, collection: Collection, *, obj_in: dict) -> dict:
        inserted_id = collection.insert_one(obj_in).inserted_id
        return collection.find_one({"_id": inserted_id})


    def get(self, collection: Collection, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(collection.find().skip(skip).limit(limit))

    def get_by_author_id(self, db: Collection, id: int):
        return db.find_one({"_id": ObjectId(id)})


    def update(self, collection: Collection, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(db_obj, dict):
            query = {"_id": db_obj.get("_id")}  # Assuming the db_obj dictionary contains the '_id' of the document
        else:
            raise ValueError("db_obj must be a dictionary with an '_id' field")

        if isinstance(obj_in, dict):
            update_data = {"$set": obj_in}
        else:
            raise ValueError("obj_in must be a dictionary representing update data")

        result = collection.update_one(query, update_data)
        if result.matched_count > 0:
            # Apply the update to db_obj to mimic the refresh in SQLAlchemy
            for key, value in obj_in.items():
                db_obj[key] = value
            return db_obj
        else:
            raise ValueError("Document with the given _id not found in the collection")


author_plain = CRUDAuthor()
