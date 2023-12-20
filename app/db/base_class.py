import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app.db.session import engine
from sqlalchemy import Column,DateTime
from sqlalchemy.types import SmallInteger
from sqlalchemy.sql import func
from datetime import date, datetime, timedelta
from pymongo import MongoClient


class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry,bind=engine)



    def __tablename__(self) -> str:
        return self.__class__.__name__.lower()

    def save(self, db_collection):
        db_collection.insert_one(self.__dict__)

    def update(self, db_collection, query):
        db_collection.update_one(query, {'$set': self.__dict__})

    def delete(self, db_collection, query):
        db_collection.delete_one(query)


@as_declarative(class_registry=class_registry,bind=engine)
class Base:
    id: t.Any
    __name__: str
    

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
