#from fastapi.encoders import jsonable_encoder
#from app.db.base_class import Base
#
#import pytest
#from fastapi.responses import JSONResponse
#from app.schemas.book import BookCreate, BookUpdate
#from app.models.book import Book
#from app.models.author import Author
#from app.crud.crud_book import *
#
#
#from datetime import date
#import pytest
#from typing import Any, Dict, List, TypeVar, Union
#
#
#from typing import Any, Dict, TypeVar
#
#from app.crud.base import CRUDBase
#from sqlalchemy.orm import Session
#
#
#def crud_book() -> CRUDBook:
#    return CRUDBook(Book)
#
#TModel = TypeVar("TModel", bound=Base)
#TCreateSchema = TypeVar("TCreateSchema", bound=BookCreate)
#TUpdateSchema = TypeVar("TUpdateSchema", bound=BookUpdate)
#
#
#class CRUDBook(CRUDBase[TModel, TCreateSchema, TUpdateSchema]):
#    def update(
#        self, db: Session, *, db_obj: Book, obj_in: Union[Book, Dict[str, Any]]
#    ) -> Book:
#        # db_obj.created_at = date.today()
#        return super().update(db, db_obj=db_obj, obj_in=obj_in)
#
#
#@pytest.fixture
#def crud_book() -> CRUDBook:
#    return CRUDBook(Book, BookCreate, BookUpdate)
#
#
#def test_update_no_error(crud_book: CRUDBook, db: Session, book: Book):
#    updated_book = crud_book.update(db, db_obj=book, obj_in=book)
#    assert updated_book is not None
#
#
#def test_update_with_dict_as_input(crud_book: CRUDBook, db: Session, book: Book):
#    input_data: Dict[str, Any] = {
#        "title": "Updated test",
#        "description": "Updated Description",
#        "publication_date": "2022-10-10",
#        "author_id": 2,
#    }
#    updated_book = crud_book.update(db, db_obj=book, obj_in=input_data)
#    assert updated_book.title == "Updated test"
#    assert updated_book.description == "Updated Description"
#    assert str(updated_book.publication_date) == "2022-10-10"
#    assert updated_book.author_id == 2
#
#
#def test_update_with_empty_dict(crud_book: CRUDBook, db: Session, book: Book):
#    input_data: Dict[str, Any] = {}
#    updated_book = crud_book.update(db, db_obj=book, obj_in=input_data)
#    assert updated_book is not None
#
#error_log
#
#
#configfile: pytest.ini
#