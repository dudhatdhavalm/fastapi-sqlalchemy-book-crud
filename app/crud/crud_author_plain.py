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
from typing import Dict, Any, Union
































class CRUDAuthor:

    
    def create(self, db: Collection, *, obj_in_data: dict) -> dict:
        """
        Creates a new document in the Authors collection.
        
        :param db: PyMongo Collection instance representing authors collection
        :param obj_in_data: Dictionary with the input data for the new author
        :return: The created author document
        """
        result = db.insert_one(obj_in_data)
        new_author = db.find_one({"_id": result.inserted_id})
        return new_author


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))


    def get_by_author_id(self, db: Collection, author_id: int):
        return db.find_one({"_id": ObjectId(str(author_id))})

    def update(self, collection: Collection, *, db_obj_id: str, obj_in: Union[Dict[str, Any], 'Author']) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = {'$set': obj_in}
        else:
            update_data = {'$set': obj_in.dict(exclude_unset=True)}

        result = collection.find_one_and_update(
            {"_id": ObjectId(db_obj_id)}, 
            update_data, 
            return_document=True
        )
        return result


author_plain = CRUDAuthor()
