from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer , String
from app.db.base_class import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer,primary_key=True)
    name = Column(String)
