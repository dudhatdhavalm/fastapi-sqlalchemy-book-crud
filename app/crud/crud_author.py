from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo.collection import Collection
from typing import List
from bson.objectid import ObjectId
from typing import Any, Dict, Union
from bson import ObjectId
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: Collection, *, obj_in: dict) -> dict:
        inserted_id = db.insert_one(obj_in).inserted_id
        db_obj = db.find_one({'_id': inserted_id})
        return db_obj


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))


    def get_by_author_id(self, collection: Collection, id: int):
        return collection.find_one({"_id": ObjectId(str(id))})

    def update(self, db: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any], None]) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = {k: v for k, v in obj_in.items() if v is not None}
        else:
            update_data = jsonable_encoder(obj_in)

        result = db.find_one_and_update(
            {"_id": db_obj_id},
            {"$set": update_data},
            return_document=True
        )
        return result

author = CRUDAuthor(Author)
