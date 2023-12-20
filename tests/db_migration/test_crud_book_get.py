#from sqlalchemy.orm import Session
#
#import pytest
#from app.db.base_class import Base
#from fastapi.encoders import jsonable_encoder
#from app.schemas.book import BookCreate
#from fastapi.responses import JSONResponse
#
#
#from typing import List
#from sqlalchemy import create_engine
#from app.models.book import Book
#from app.models.author import Author
#from app.crud.crud_book import *
#from sqlalchemy.orm import Session, sessionmaker
#from typing import Any, Dict, List, TypeVar, Union
#
#
#from typing import Type
#from datetime import date
#from app.crud.base import CRUDBase
#
#
#class CRUDBook(CRUDBase):
#    def __init__(self, model: Type[Base]) -> None:
#        self.model = model
#
#    def get(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Book]:
#        return db.query(self.model).offset(skip).limit(limit).all()
#
#DATABASE_URL = "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#
#engine = create_engine(DATABASE_URL)
#TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
#@pytest.fixture
#def db() -> Session:
#    # connect to the database
#    session = TestingSessionLocal()
#    yield session
#    session.close()
#
#
#def test_get_does_not_error(db: Session) -> None:
#    crud_book_instance = CRUDBook(Book)
#    result = crud_book_instance.get(db)
#    assert result is not None
#
#
#def test_get_returns_list(db: Session) -> None:
#    crud_book_instance = CRUDBook(Book)
#    result = crud_book_instance.get(db)
#    assert isinstance(result, List)
#
#
#def test_get_returns_book_list(db: Session) -> None:
#    crud_book_instance = CRUDBook(Book)
#    result = crud_book_instance.get(db)
#    if result:
#        assert isinstance(result[0], Book)
#