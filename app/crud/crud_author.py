from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo.collection import Collection
from bson import ObjectId
from typing import List
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: Collection, *, obj_in: AuthorCreate) -> dict:
        author_data = obj_in.dict(by_alias=True)  # Convert Pydantic model to dictionary
        result = db.insert_one(author_data)
        new_author = db.find_one({"_id": result.inserted_id})
        return new_author


    def get(self, db: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.find().skip(skip).limit(limit))

    
    def get_by_author_id(self, db: Collection, id: int):
        return db.find_one({'_id': ObjectId(id)})


    def update(self, db_collection: Collection, *, db_obj_id: str, obj_in: Union[Dict[str, Any], Author]) -> Dict:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = jsonable_encoder(obj_in)

        db_collection.update_one({'_id': ObjectId(db_obj_id)}, {'$set': update_data})
        new_db_obj = db_collection.find_one({'_id': ObjectId(db_obj_id)})
        return new_db_obj

author = CRUDAuthor(Author)
