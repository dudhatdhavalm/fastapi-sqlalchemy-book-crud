from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from bson import json_util
from typing import List
from pymongo.collection import Collection
from typing import Optional
from typing import Any, Dict, Union
from bson import ObjectId
































class CRUDAuthor:

    def create(self, db, *, obj_in: dict) -> dict:
        db_obj = db.Author.insert_one(json_util.loads(obj_in))
        new_author = db.Author.find_one({"_id": db_obj.inserted_id})
        return new_author

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Author]:
        authors_cursor = collection.find().skip(skip).limit(limit)
        return list(authors_cursor)


    def get_by_author_id(self, collection: Collection, id: int) -> Optional[dict]:
        return collection.find_one({"_id": id})

    
    def update(self, collection: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], None]) -> Dict[str, Any]:
        if obj_in is not None:
            update_data = {k: v for k, v in obj_in.items() if v is not None}
            result = collection.update_one({'_id': db_obj_id}, {'$set': update_data})
            if result.modified_count > 0:
                updated_document = collection.find_one({'_id': db_obj_id})
                return updated_document
            else:
                # Nothing was updated.
                return {}
        else:
            # obj_in is None, so no update will be performed.
            return {}


author_plain = CRUDAuthor()
