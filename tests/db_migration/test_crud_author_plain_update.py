#from typing import Any, Dict, Union
#from fastapi.encoders import jsonable_encoder
#from app.models.author import Author
#from datetime import date
#from sqlalchemy.orm import Session, sessionmaker
#from sqlalchemy import create_engine
#from app.crud.crud_author_plain import CRUDAuthor
#from app.schemas.author import AuthorCreate
#
#from app.models.author import Author
#
#from app.crud.crud_author_plain import *
#
#import pytest
#
#
#from datetime import date
#
#
#@pytest.fixture
#def db_obj() -> Author:
#    return Author(name="Example", birth_date=date.today())
#
#
#@pytest.fixture
#def session() -> Session:
#    engine = create_engine("postgresql://postgres:root@host.docker.internal:5432/")
#    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#    return SessionLocal()
#
#
#def test_CRUDAuthor_update_no_errors(db_obj: Author, session: Session) -> None:
#    crud_author = CRUDAuthor()
#    obj_in_data = jsonable_encoder(db_obj)
#    result = crud_author.update(db=session, db_obj=db_obj, obj_in=obj_in_data)
#    assert result is not None
#
#
#def test_CRUDAuthor_update_empty_update_data(db_obj: Author, session: Session) -> None:
#    crud_author = CRUDAuthor()
#    result = crud_author.update(db=session, db_obj=db_obj, obj_in={})
#    assert result is not None
#
#
#def test_CRUDAuthor_update_invalid_fields(db_obj: Author, session: Session) -> None:
#    crud_author = CRUDAuthor()
#    with pytest.raises(Exception):
#        crud_author.update(
#            db=session, db_obj=db_obj, obj_in={"non_existing_field": "value"}
#        )
#