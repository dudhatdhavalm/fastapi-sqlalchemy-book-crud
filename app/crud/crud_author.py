from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from bson import ObjectId
from pymongo.collection import Collection
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, collection: Collection, *, obj_in: AuthorCreate) -> dict:
        obj_in_data = jsonable_encoder(obj_in)
        inserted_id = collection.insert_one(obj_in_data).inserted_id
        new_obj = collection.find_one({"_id": inserted_id})
        return new_obj

    
    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = collection.find().skip(skip).limit(limit)
        authors = list(cursor)
        return authors


    def get_by_author_id(self, db: Collection, id: int):
        return db.find_one({'_id': id})

    
    def update(self, collection: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], ObjectId]) -> Dict[str, Any]:
        if isinstance(obj_in, ObjectId):
            obj_in = {'_id': obj_in}
        updated_values = {"$set": obj_in}
        result = collection.update_one({'_id': db_obj_id}, updated_values)
        if result.matched_count:
            return collection.find_one({'_id': db_obj_id})
        raise ValueError(f"Document with id {db_obj_id} not found.")        

author = CRUDAuthor(Author)
