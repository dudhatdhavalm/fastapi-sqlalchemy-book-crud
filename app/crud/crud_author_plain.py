from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from datetime import date
from pymongo.collection import Collection
from typing import List, Dict
from typing import Any, Dict, Union
































class CRUDAuthor:

    def create(self, db: Collection, *, obj_in: dict) -> dict:
        # obj_in is expected to be a dictionary that represents an Author object
        result = db.insert_one(obj_in)
        # Create the created author with the inserted ID
        created_author = db.find_one({"_id": result.inserted_id})
        return created_author

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict]:
        return list(collection.find().skip(skip).limit(limit))


    def get_by_author_id(self, mongo_collection: Collection, id: int) -> Dict:
        return mongo_collection.find_one({"_id": id})

    
    def update(self, db: Collection, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict]) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            update_data = {'$set': obj_in}
        else:
            update_data = {'$set': obj_in.to_mongo()}
        
        updated_result = db.find_one_and_update(
            {'_id': db_obj['_id']}, 
            update_data, 
            return_document=True
        )
        return updated_result


author_plain = CRUDAuthor()
