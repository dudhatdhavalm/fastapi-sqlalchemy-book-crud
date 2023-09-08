from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder

class CRUDAuthor(CRUDBase[Author,AuthorCreate,None]):
    def create(self, db: Session, *, obj_in: AuthorCreate, created_by=None) -> Author:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
author = CRUDAuthor(Author)
