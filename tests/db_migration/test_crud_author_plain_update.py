#
#import pytest
#from fastapi.encoders import jsonable_encoder
#from sqlalchemy.orm.exc import UnmappedInstanceError
#from sqlalchemy import create_engine
#from app.crud.crud_author_plain import CRUDAuthor
#from app.schemas.author import AuthorCreate
#from app.models.author import Author
#
#
#import os
#from sqlalchemy.orm import Session, sessionmaker
#import pytest
#from typing import Any, Dict
#from app.crud.crud_author_plain import *
#from datetime import date
#
#
#class CRUDAuthor:
#    def update(
#        self,
#        db: Session,
#        *,
#        db_obj: Author,
#        obj_in: Union[AuthorCreate, Dict[str, Any]]
#    ) -> Author:
#        obj_data = jsonable_encoder(db_obj)
#        if isinstance(obj_in, dict):
#            update_data = obj_in
#        else:
#            update_data = obj_in.dict(exclude_unset=True)
#
#        for field in obj_data:
#            if field in update_data:
#                setattr(db_obj, field, update_data[field])
#
#        db.add(db_obj)
#        db.commit()
#        db.refresh(db_obj)
#        return db_obj
#
#
#@pytest.fixture
#def db() -> Session:
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()
#
#
#def test_update_no_error(db: Session):
#    crud_author = CRUDAuthor()
#    db_obj = Author(id=1, name="John Doe", birthdate=date.today())
#    db.add(db_obj)
#    db.commit()
#
#    new_data = {"name": "Jane Doe"}
#    result = crud_author.update(db, db_obj=db_obj, obj_in=new_data)
#    assert result is not None
#
#
#def test_update_correct_author(db: Session):
#    crud_author = CRUDAuthor()
#    old_author = Author(id=1, name="John Doe", birthdate=date.today())
#    db.add(old_author)
#    db.commit()
#
#    new_data = {"name": "Jane Doe"}
#    updated_author = crud_author.update(db, db_obj=old_author, obj_in=new_data)
#    assert updated_author.name == "Jane Doe"
#
#
#def test_update_invalid_author(db: Session):
#    crud_author = CRUDAuthor()
#    fake_author = Author(id=-1, name="Fake Author", birthdate=date.today())
#    with pytest.raises(UnmappedInstanceError):
#        crud_author.update(db, db_obj=fake_author, obj_in={"name": "Fake Author 2"})
#
#
#def test_update_obj_in_instance(db: Session):
#    crud_author = CRUDAuthor()
#    old_author = Author(id=1, name="John Doe", birthdate=date.today())
#    db.add(old_author)
#    db.commit()
#
#    new_author = AuthorCreate(name="Jane Doe")
#    updated_author = crud_author.update(db, db_obj=old_author, obj_in=new_author)
#    assert updated_author.name == "Jane Doe"
#