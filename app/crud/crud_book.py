from typing import TypeVar
from app.models.book import Book
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.schemas.book import BookCreate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.db.base_class import Base
ModelType = TypeVar("ModelType", bound=Base)

class CRUDBook(CRUDBase[Book,BookCreate,None]):
    def create(self, db: Session,*, obj_in: BookCreate , created_by=None) -> Book:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return JSONResponse(
            status_code=200, content={"status_code": 200, "message": "success"}
        )

book = CRUDBook(Book)