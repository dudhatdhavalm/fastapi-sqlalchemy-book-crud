from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from app.db.base_class import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    pages = Column(Integer)
    created_at = Column(Date)
    author_id = Column(
        Integer,
        ForeignKey('authors.id'), nullable=True
    )
