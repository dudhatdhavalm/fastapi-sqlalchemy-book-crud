from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict, List, Union


class CRUDAuthor(CRUDBase[Author, AuthorCreate, None]):
    def create(self, db: Session, *, obj_in: AuthorCreate) -> Author:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Author]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_by_author_id(self,db:Session,id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, *, db_obj: Author, obj_in: Union[Author,Dict[str, Any]]) -> Author:
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

author = CRUDAuthor(Author)
