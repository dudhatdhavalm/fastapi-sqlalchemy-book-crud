#from pydantic import BaseModel
#
#import pytest
#from app.db.base_class import Base
#from typing import Type
#from sqlalchemy.orm import Session, sessionmaker
#from sqlalchemy import Column, Integer, String, create_engine
#from app.crud.base import *
#from app.crud.base import CRUDBase
#
#
#class CreateSchemaType(BaseModel):
#    name: str
#    description: str
#
#
#class ModelType(Base):
#    __tablename__ = "modeltype"
#    id = Column(Integer, primary_key=True, index=True)
#    name = Column(String)
#    description = Column(String)
#
#
## creating a new session for database operations
#engine = create_engine(
#    "postgresql://root:postgres@localhost:5432/code_robotics_1701690361803",
#    pool_pre_ping=True,
#)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#db: Session = SessionLocal()
#
#
#crud_base = CRUDBase(ModelType)
#new_obj = CreateSchemaType(name="Test", description="Test description")
#
#
#@pytest.fixture(scope="module")
#def db_setup():
#    Base.metadata.create_all(bind=engine)
#    yield
#    Base.metadata.drop_all(bind=engine)
#
#
#@pytest.mark.usefixtures("db_setup")
#def test_create():
#    db_obj = crud_base.create(db, obj_in=new_obj)
#    assert db_obj is not None
#    assert db_obj.name == "Test"
#    assert db_obj.description == "Test description"
#
#
#@pytest.mark.usefixtures("db_setup")
#def test_create_with_created_by():
#    db_obj = crud_base.create(db, obj_in=new_obj, created_by="Test User")
#    assert db_obj is not None
#    assert db_obj.name == "Test"
#    assert db_obj.description == "Test description"
#    assert db_obj.created_by == "Test User"
#
#
#class ModelType(Base):
#    __tablename__ = "modeltype"
#    id = Column(Integer, primary_key=True, index=True)
#    name = Column(String)
#    description = Column(String)
#    created_by = Column(String)
#
#
#class CreateSchemaType(BaseModel):
#    name: str
#    description: str
#    created_by: Optional[str] = None
#
#
#@pytest.mark.usefixtures("db_setup")
#def test_create_with_created_by():
#    db_obj = crud_base.create(db, obj_in=new_obj, created_by="Test User")
#    assert db_obj is not None
#    assert db_obj.name == "Test"
#    assert db_obj.description == "Test description"
#