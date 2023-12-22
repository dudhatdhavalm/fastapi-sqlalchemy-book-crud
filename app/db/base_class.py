import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from app.db.session import engine
from sqlalchemy import Column,DateTime
from sqlalchemy.types import SmallInteger
from sqlalchemy.sql import func
from datetime import date, datetime, timedelta
from datetime import datetime
from bson.objectid import ObjectId


class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry,bind=engine)


    def __tablename__(cls) -> str:
        """
        Generates a collection name automatically based on the class name.
        This is just a utility method to standardize collection names and
        does not have a direct effect on pymongo interactions.
        """
        return cls.__name__.lower()

    # Instead of declared attributes, pymongo uses dictionaries to represent documents
    # The BaseDefault class serves as a schema guideline, so we create properties that
    # we expect to be in our MongoDB documents, along with possible default values.

    @property
    def schema(self) -> dict:
        """
        Serves as an illustration of a default document structure for MongoDB collections.
        """
        return {
            '_id': ObjectId(),
            'created_at': datetime.utcnow(),
            # Any other default fields can be added here
        }


@as_declarative(class_registry=class_registry,bind=engine)
class Base:
    id: t.Any
    __name__: str
    

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
