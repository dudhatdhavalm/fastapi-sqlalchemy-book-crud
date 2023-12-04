#from sqlalchemy.orm import Session
#
#import pytest
#from fastapi.encoders import jsonable_encoder
#
#
#from typing import Dict, Union
#from app.tests.utils.utils import random_lower_string
#from sqlalchemy import create_engine
#from app.schemas.author import AuthorCreate
#from app.models.author import Author
#from typing import Any, Dict, List, Union
#from app.crud.crud_author import CRUDAuthor
#from app.crud.base import CRUDBase
#from sqlalchemy.orm import Session, sessionmaker
#from app.crud.crud_author import *
#
#
#class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorCreate]):
#    def update(
#        self, db: Session, *, db_obj: Author, obj_in: Union[Author, Dict[str, Any]]
#    ) -> Author:
#        return super().update(db, db_obj=db_obj, obj_in=obj_in)
#
#SQLALCHEMY_DATABASE_URL = (
#    "postgresql://root:postgres@localhost/code_robotics_1701690361803"
#)
#
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
#
#@pytest.fixture
#def db_session() -> Session:
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    db = SessionLocal()
#    yield db
#    db.close()
#
#
#@pytest.fixture()
#def test_author(db_session: Session) -> Author:
#    author = Author(name=random_lower_string())
#    db_session.add(author)
#    db_session.commit()
#    db_session.refresh(author)
#    return author
#
#
#@pytest.fixture
#def update_author() -> Dict[str, Union[str, int]]:
#    return {"name": random_lower_string()}
#
#
#def test_update(db_session, test_author, update_author):
#    crud_author = CRUDAuthor()
#    updated_author = crud_author.update(
#        db=db_session, db_obj=test_author, obj_in=update_author
#    )
#    assert updated_author is not None
#    assert updated_author.name == update_author["name"]
#
#
#def test_update_object_in(db_session, test_author):
#    crud_author = CRUDAuthor()
#    updated_author = crud_author.update(
#        db=db_session, db_obj=test_author, obj_in=test_author
#    )
#    assert updated_author is not None
#    assert updated_author.name == test_author.name
#