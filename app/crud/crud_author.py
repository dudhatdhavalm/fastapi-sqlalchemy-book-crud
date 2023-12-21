from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo.collection import Collection
from typing import List
from bson import ObjectId
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, collection: Collection, *, obj_in: AuthorCreate) -> dict:
        # In pymongo you don't need to encode the object, you can directly insert a dictionary
        obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        # Inserting the new document into the collection and getting back the inserted_id
        inserted_id = collection.insert_one(obj_in_data).inserted_id
        # Retrieving the inserted document from the database
        db_obj = collection.find_one({'_id': inserted_id})
        return db_obj

    def get(self, collection: Collection, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(collection.find().skip(skip).limit(limit))

    def get_by_author_id(self, collection: Collection, id: int):
        return collection.find_one({'_id': id})


    def update(self, collection: Collection, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], AuthorCreate]) -> Dict[str, Any]:
        if isinstance(db_obj, dict):
            # ensure we have an ObjectId if it's in string format
            if '_id' in db_obj and isinstance(db_obj['_id'], str):
                db_obj['_id'] = ObjectId(db_obj['_id'])
            query = {'_id': db_obj['_id']}
        else:
            raise ValueError("db_obj must be a dictionary with an '_id' key")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Convert obj_in (of type AuthorCreate) to a dictionary
            update_data = obj_in.dict(exclude_unset=True)

        updated_result = collection.update_one(query, {'$set': update_data})
        if updated_result.modified_count == 1:
            return collection.find_one(query)
        else:
            # Handle the case where the document was not updated
            return None

author = CRUDAuthor(Author)
