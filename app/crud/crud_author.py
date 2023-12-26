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

    def create(self, collection: Collection, *, obj_in: dict) -> dict:
        # Since pymongo works directly with dictionaries, there is no need to encode the object as JSON
        result = collection.insert_one(obj_in)
        # The inserted ID is retrieved and used to return the full document from the database
        new_author = collection.find_one({'_id': result.inserted_id})

        # Convert '_id' from ObjectId to string, for easier use in JSON responses
        if '_id' in new_author:
            new_author['_id'] = str(new_author['_id'])

        return new_author

    
    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return list(collection.find().skip(skip).limit(limit))


    def get_by_author_id(self, db: Collection, id: int):
        return db.find_one({"_id": id})

    
    def update(self, collection: Collection, *, db_obj_id: str, obj_in: Union[Dict[str, Any], None]) -> Dict[str, Any]:
        if isinstance(obj_in, dict):
            # Update the document with the given ID using the new values provided in obj_in
            result = collection.update_one({"_id": ObjectId(db_obj_id)}, {"$set": obj_in})
        else:
            raise ValueError("The 'obj_in' parameter must be a dictionary")

        # Return the updated document
        return collection.find_one({"_id": ObjectId(db_obj_id)})

author = CRUDAuthor(Author)
