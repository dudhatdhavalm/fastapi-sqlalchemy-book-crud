from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo.collection import Collection
from bson import ObjectId
from typing import List, Dict
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, collection: Collection, *, obj_in: dict) -> dict:
        obj_in_data = jsonable_encoder(obj_in)
        result = collection.insert_one(obj_in_data)
        new_id = result.inserted_id
        new_author = collection.find_one({"_id": new_id})
        return new_author


    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        return list(collection.find().skip(skip).limit(limit))


    def get_by_author_id(self, db: Collection, id: int) -> Dict:
        return db.find_one({'_id': ObjectId(str(id))})


    def update(self, collection: Collection, *, db_obj_id: ObjectId, obj_in: Union[Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = {k: v for k, v in obj_in.items() if v is not None}

        updated_result = collection.find_one_and_update(
            {'_id': db_obj_id},
            {'$set': update_data},
            return_document=True
        )

        return updated_result

author = CRUDAuthor(Author)
