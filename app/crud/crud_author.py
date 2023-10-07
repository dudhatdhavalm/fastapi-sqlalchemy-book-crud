from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union
from pymongo import MongoClient
from typing import List
from typing import Any, Dict, Union
































class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):

    def create(self, db: MongoClient, *, obj_in: AuthorCreate) -> Dict:
        obj_in_data = jsonable_encoder(obj_in)
        collection = db['Author']
        result = collection.insert_one(obj_in_data)
        return obj_in_data


    def get_all(self, db: MongoClient, *, skip: int = 0, limit: int = 100) -> List[dict]:
        return list(db.authors.find().skip(skip).limit(limit))


    def get(self,db:MongoClient,id: int):
        return db.authors.find_one({"id": id})


    def update(self, db: MongoClient, *, db_obj: Dict[str, Any], obj_in: Union[Dict[str, Any], Dict[str, Any]]) -> Dict[str, Any]:
        db_obj.update(obj_in)
        db['author'].replace_one({"_id": db_obj['_id']}, db_obj)

        return db_obj

author = CRUDAuthor(Author)
